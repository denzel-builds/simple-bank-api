from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Our Custom User
# We inherit from AbstractUser so we keep the built-in username/password/email logic
class User(AbstractUser):
    # We can add fields here later (like ID number or Phone Number)
    pass

# 2. The Bank Account
class BankAccount(models.Model):
    # Link this account to one specific User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    
    # Account details
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.balance}"
