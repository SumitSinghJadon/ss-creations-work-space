from django.views import View
from django.shortcuts import render


class PermissionView(View):
    def get(self, request):
        context = {}
        return render(request, 'permission.html', context)

    def post(self, request):
        pass 

