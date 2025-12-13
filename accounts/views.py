from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BankAccount
from .serializers import BankAccountSerializer
from django.db import transaction
from .models import Transaction
from .serializers import TransferSerializer

class AccountDetailView(APIView):
    # Security Gate: Only logged-in users can access this
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Who is asking? (Django knows this automatically from the login)
        user = request.user
        
        try:
            # 2. Find the account linked to this specific user
            # We can use 'user.account' because of the related_name we set in models.py
            account = user.account 
        except BankAccount.DoesNotExist:
            return Response({"error": "You do not have a bank account yet."}, status=404)

        # 3. Translate the python object to JSON
        serializer = BankAccountSerializer(account)
        
        # 4. Send the response
        return Response(serializer.data)
    
class TransferFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Validate the Input
        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Get cleaned data
        receiver_account_num = serializer.validated_data['account_number']
        amount = serializer.validated_data['amount']
        sender_account = request.user.account

        # 2. The Logic Checks
        if sender_account.balance < amount:
            return Response({"error": "Insufficient funds"}, status=400)
        
        try:
            receiver_account = BankAccount.objects.get(account_number=receiver_account_num)
        except BankAccount.DoesNotExist:
            return Response({"error": "Receiver account not found"}, status=404)

        # 3. THE ATOMIC BLOCK (The Safety Bubble)
        try:
            with transaction.atomic():
                # Step A: Subtract from Sender
                sender_account.balance -= amount
                sender_account.save()

                # Step B: Add to Receiver
                receiver_account.balance += amount
                receiver_account.save()

                # Step C: Create the Record
                Transaction.objects.create(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount
                )
        except Exception as e:
            # If ANYTHING fails inside the 'with' block, the DB rolls back here automatically.
            return Response({"error": str(e)}, status=500)

        return Response({"message": "Transfer successful"}, status=200)
