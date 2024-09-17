from django.views import View
from django.shortcuts import redirect, render


class Restricted(View):
    def get(self, request):
        return render(request, 'auth/restricted.html')
