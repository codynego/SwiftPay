from django.db import models
from users.models import User
from uuid import uuid4

class Account(models.Model):
    """ACCOUNT_TYPE = (
        ('savings', 'savings'),
        ('current', 'current'),
    )"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50, default='NGN', null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('tranfer', 'transfer'),
        ('deposit', 'deposit')
    )
    TRANSACTION_STATUS = (
        ('completed', 'completed'),
        ('pending', 'pending'),
        ('failed', 'failed')
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transaction', null=True)
    beneficiary_username = models.CharField(max_length=255, blank=True, null=True,)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    trans_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    paystack_payment_reference = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.account.user.__str__()
    


class BasePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)


class paymentlinks(BasePayment):
    link = models.URLField(max_length=50)

class PaymentQrcode(BasePayment):
    qrcode = models.ImageField(upload_to='img')


class PaymentRequest(models.Model):
    REQUEST_CHOICES = (
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('pending', 'pending')
    )
    uid = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    recipient = models.CharField(max_length=100, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=REQUEST_CHOICES, default='pending')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)