from django.db import models
from users.models import User
from django.utils import timezone
import random
import string


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.IntegerField(blank=False)
    created = models.DateTimeField(auto_now=True)


    def is_expired(self):
        current_time = timezone.now()
        duration = current_time - self.created
        return duration.total_seconds() >= 300
    
    @staticmethod
    def generate_otp(user):
        length = 6
        characters = string.digits  # Use digits (0-9) for OTP generation
        otp = ''.join(random.choice(characters) for _ in range(length))

        OTP.objects.filter(user=user).delete()
        otp_user = OTP.objects.create(user=user, otp_code=otp)
        otp_user.save()
        return otp
    