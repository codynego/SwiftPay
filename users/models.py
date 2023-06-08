from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pin = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    bvn = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='img', blank=True, null=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.username
    
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    
