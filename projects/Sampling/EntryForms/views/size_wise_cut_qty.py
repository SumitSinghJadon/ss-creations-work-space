from django.views import View
from django.shortcuts import render

class SizeWiseCutQtyView(View):
    def get(self, request):
        return render(request, 'size_wise_cut_qty.html')