from django.contrib import admin
from .models import User, BankAccount, Transaction

# This tells the Admin panel: "Please let me manage these tables"
admin.site.register(User)
admin.site.register(BankAccount)
admin.site.register(Transaction)
