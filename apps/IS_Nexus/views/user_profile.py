from django.views import View
from IntelliSync_db.models import User
from django.shortcuts import redirect, render


class UserProfile(View):
    def get(self, request):
        return render(request, 'auth/user_profile.html') 

    def post(self, request):
        return render(request, 'auth/user_profile.html') 
