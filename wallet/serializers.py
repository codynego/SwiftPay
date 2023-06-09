from rest_framework import serializers
from .models import Account, Transaction, PaymentRequest
from users.serializers import UserSerializer
from .tasks import initialize_transaction_task
from users.models import User
from .utils import update_account

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'balance']



class PaymentSerializer(serializers.ModelSerializer):
    pin = serializers.IntegerField(write_only=True)
    class Meta:
        model = Transaction
        fields = ['beneficiary_username', 'amount', 'description', 'status', 'created_at', 'pin']
        read_only_fields = ('created_at', 'status')

    def get_pin(self, instance):
        return instance.account.user.pin


    def create(self, attrs):
        #beneficiary_account_number = attrs['beneficiary_account_number']
        beneficiary_username = attrs['beneficiary_username']
        amount = attrs['amount']
        description = attrs['description']
        pin = attrs['pin']
        
        user = self.context.get('request')

        if user.pin != pin:
            raise serializers.ValidationError('invalid pin')
        if Account.objects.filter(user=user).exists():
            sender_account = Account.objects.get(user=user)
        else:
            raise serializers.ValidationError('no user found')
        if sender_account.balance < amount:
            raise serializers.ValidationError('insuffiecient funds')
        if sender_account.user.username == beneficiary_username:
            raise serializers.ValidationError('invalid transaction')

        beneficiary = User.objects.get(username=beneficiary_username)
        
        payment = update_account(amount, user, beneficiary,
                                        description, "transfer")


        return payment
    

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('account',)


class DepositSerializer(serializers.Serializer):

    amount = serializers.IntegerField()
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError({"detail": f"Email not found"})

    def save(self):
        user = self.context['request'].user
        account = Account.objects.get(user=user)
        data = self.validated_data
        response = initialize_transaction_task(data, account)
        return response
    

class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        exclude = ('sender',)
        read_only_fields = ('status', 'created_at', 'updated_at', 'uid')

    
    def create(self, attrs):
        user = self.context['request']
        recipient = attrs['recipient']
        amount = attrs['amount']
        description = attrs['description']

        if User.objects.filter(username=recipient).exists():
            paymentrequest = PaymentRequest(
            sender = user,
            recipient=recipient,
            amount=amount,
            description=description,
        )
            paymentrequest.save()
        else:
            raise serializers.ValidationError({'message': 'recipient doesnt exist'})
        return paymentrequest