from django.views import View
from django.shortcuts import render

class DispatchEntryView(View):
    def get(self, request):
        return render(request, 'dispatch_entry.html')