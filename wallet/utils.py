from .models import Account, Transaction
from users.models import User
from decimal import Decimal
import random
import string


def update_account(amount: int, sender: User,
                   recipient: str, description: str, 
                   trans_type: str) -> bool:
    """
    A function that updates the accounts users

    Args:
        amount (int): the amount to update
        sender (User): the user to subtract from
        recipient: the recipient to update
    """
    try:
        sender_account = Account.objects.get(user=sender)
        recipient_account = Account.objects.get(user=recipient)
    except:
        return False

    sender_account.balance -= Decimal(amount)
    recipient_account.balance += Decimal(amount)
    sender_account.save()
    recipient_account.save()
    transaction = Transaction.objects.create(
        account = sender_account,
        beneficiary_username = recipient.username,
        amount = amount,
        description = description,
        status='completed',
        trans_type = trans_type,
    )
    transaction.save()
    return transaction


def generate_code():
    length = 8
    letters = string.ascii_letters
    digits = string.digits
    characters = letters + digits 
    code = ''.join(random.choice(characters) for _ in range(length))
    return code
