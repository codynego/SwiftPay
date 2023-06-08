from django.contrib import admin
from .models import Account, Transaction, Payment, PaymentRequest

# Register your models here.

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(PaymentRequest)
