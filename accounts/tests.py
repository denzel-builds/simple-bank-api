from django.urls import reverse
from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, BankAccount

class TransferTests(APITestCase):
    def setUp(self):
        # This runs BEFORE every single test. We set up the stage.
        
        # 1. Create User A (Sender)
        self.user_a = User.objects.create_user(username='sender', password='password123')
        self.account_a = BankAccount.objects.create(
            user=self.user_a, 
            account_number='11111', 
            balance=Decimal('1000.00')
        )

        # 2. Create User B (Receiver)
        self.user_b = User.objects.create_user(username='receiver', password='password123')
        self.account_b = BankAccount.objects.create(
            user=self.user_b, 
            account_number='22222', 
            balance=Decimal('500.00')
        )

        # 3. The URL we are testing
        self.url = reverse('transfer-funds') # This looks up the name='transfer-funds' in urls.py

    def test_transfer_money_success(self):
        # 1. Force authentication (Log in as User A)
        self.client.force_authenticate(user=self.user_a)

        # 2. Define the data to send
        data = {
            "account_number": "22222", # Sending to User B
            "amount": 200.00
        }

        # 3. Make the POST request
        response = self.client.post(self.url, data)

        if response.status_code != 200:
            print("\n!!! SERVER ERROR MESSAGE !!!")
            print(response.data)  # This prints the specific error from the view
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

        # 4. ASSERTIONS (The Proof)
        # Check if the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the money actually moved in the database
        self.account_a.refresh_from_db() # Reload data from DB
        self.account_b.refresh_from_db()

        self.assertEqual(self.account_a.balance, 800.00) # 1000 - 200
        self.assertEqual(self.account_b.balance, 700.00) # 500 + 200

    def test_transfer_insufficient_funds(self):
        # Test that we CANNOT steal money we don't have
        self.client.force_authenticate(user=self.user_a)

        data = {
            "account_number": "22222",
            "amount": 5000.00 # More than balance (1000)
        }

        response = self.client.post(self.url, data)

        # Should fail with 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
