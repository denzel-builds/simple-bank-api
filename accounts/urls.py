from django.urls import path
from .views import AccountDetailView

urlpatterns = [
    # This means: if someone goes to ".../balance/", run the AccountDetailView
    path('balance/', AccountDetailView.as_view(), name='account-balance'),
]