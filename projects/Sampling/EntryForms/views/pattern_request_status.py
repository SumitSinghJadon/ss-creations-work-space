from django.views import View
from django.shortcuts import render

class PatternRequestStatusView(View):
    def get(self, request):
        return render(request, 'pattern_request_status.html')
