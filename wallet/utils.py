from .models import Account, Transaction
from users.models import User
from decimal import Decimal
import random
import string
from authentication.tasks import send_email



def walletMoneyTransferEmail(transaction: Transaction):
    subject = "You have received a payment"
    recipient_name = transaction.beneficiary
    sender_name = transaction.account.user.username
    amount = transaction.amount
    desciption = transaction.description
    app_name = "swiftPay"
    support_email = "emonenaabednego@gmail.com"

    message = f"Dear {recipient_name}\n\n\
        We're excited to inform you that you have received a payment on {app_name}. Here are the details:\n\n\
        Sender: {sender_name}\n\
        Amount: {amount}\n\
        Payment Description: {desciption}\n\
        The funds have been successfully transferred to your account. You can view the transaction details by logging into your {app_name} account.\n\n\
        Thank you for using {app_name} for your payment needs. We appreciate your trust in our platform.\n\
        Best regards,\n\n\
        If you have any questions or need further assistance, please don't hesitate to reach out to our support team at {support_email}.\n\n\
        {app_name} Team\n"
    
    recipient = User.objects.get(username=recipient_name)
    data = {'email_subject': subject,
            'email_body': message,
            'to_email': recipient.email}
    
    send_email(data)

    return True


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
        beneficiary = recipient.username,
        amount = amount,
        description = description,
        status='completed',
        trans_type = trans_type,
    )
    walletMoneyTransferEmail(transaction)
    transaction.save()
    return transaction


def generate_code():
    length = 8
    letters = string.ascii_letters
    digits = string.digits
    characters = letters + digits 
    code = ''.join(random.choice(characters) for _ in range(length))
    return code



