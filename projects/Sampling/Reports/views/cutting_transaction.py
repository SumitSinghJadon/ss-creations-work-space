from django.views import View
from django.shortcuts import render, redirect
from Sampling_db.models import CuttingEntryMt


class CuttingTransactionView(View):
    def get(self, request):
        data = CuttingEntryMt.objects.filter(is_active=True)
        context = {
            'data':data
        }
        return render(request, 'cutting_transaction.html', context)

    def post(self, request):
        return redirect('cutting_transaction_view_page')

