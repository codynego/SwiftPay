from rest_framework import serializers
from users.models import User
from .models import OTP
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=60, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'confirm_password']


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        username = attrs['username']
        email = attrs['email']

        if password != confirm_password:
            raise serializers.ValidationError("password doesnt match")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exist")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exist")
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    
class EmailVerificationSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(max_length=10)

    class Meta:
        model = OTP
        fields = ['otp_code']

class ResendVerificationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LogoutSerializer(serializers.Serializer):
    refresh_token =  serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError({'incorrect_token': 'The token is either invalid or expired'})

