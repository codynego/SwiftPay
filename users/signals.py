from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from wallet.models import Account 


@receiver(post_save, sender=User)
def auto_create_account(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(
            user = instance,
            account_number = 12345566,
            balance = 0,
        )
        account.save()