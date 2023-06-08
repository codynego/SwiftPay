from .models import Transaction, Account
import requests
from django.conf import settings
from celery import shared_task

@shared_task()
def initialize_transaction_task(data, user_account):
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
    r = requests.post(url, headers=headers, data=data)
    response = r.json()
    Transaction.objects.create(
        account=user_account,
        trans_type="deposit",
        amount= data["amount"],
        description = "wallet top-up",
        paystack_payment_reference=response['data']['reference'],
        status="pending"
    )

    return response