from django.urls import path 
from .views import CuttingTransactionView


urlpatterns = [
    path('cutting-transaction/', CuttingTransactionView.as_view(), name="cutting_transaction_view_page")
]
