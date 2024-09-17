from django.views import View
from django.shortcuts import render

class SizeWiseStitchQtyView(View):
    def get(self, request):
        return render(request, 'size_wise_stitch_qty.html')