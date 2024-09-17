from django.views import View
from django.shortcuts import redirect, render
import IS_Nexus


class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard.html')

