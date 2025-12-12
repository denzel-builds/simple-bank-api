from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BankAccount
from .serializers import BankAccountSerializer

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
