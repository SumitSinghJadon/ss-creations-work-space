from django.views import View
from django.shortcuts import render


class FinishingTransactionHistoryView(View):
    def get(self, request):
        return render(request, 'finishing_transaction_history.html')

