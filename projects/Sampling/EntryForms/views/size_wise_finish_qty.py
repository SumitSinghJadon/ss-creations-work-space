from django.views import View
from django.shortcuts import render

class SizeWiseFinishQtyView(View):
    def get(self, request):
        return render(request, 'size_wise_finish_qty.html')