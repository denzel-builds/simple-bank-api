from rest_framework import serializers
from .models import User, BankAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # We only want to show the ID and Username.
        # CRITICAL: Never show the password field here!
        fields = ['id', 'username', 'email']

class BankAccountSerializer(serializers.ModelSerializer):
    # This calls the UserSerializer to show user details within the BankAccount
    user = UserSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = ['user','account_number', 'balance']

class TransferSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)