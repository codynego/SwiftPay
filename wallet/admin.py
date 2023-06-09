from django.contrib import admin
from .models import Account, Transaction, PaymentRequest, PaymentLInk

# Register your models here.

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(PaymentRequest)
admin.site.register(PaymentLInk)
