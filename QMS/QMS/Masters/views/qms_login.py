from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from IntelliSync_db.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
from QMS_db.models import DefectMaster ,ProcessMaster
import json
from django.shortcuts import get_object_or_404

def logout_user(request):
    logout(request)
    messages.warning(request, "Logout Success, Please Login again.")
    return redirect("login_page")


def login_user_without_password(request, username):
    user = User.objects.get(username='admin')
    login(request, user)
    
    
    
class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_page = request.GET.get("next") or "module_dashboard"
        current_url = request.build_absolute_uri()

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'user': username, 'next': next_page})
            else:
                return JsonResponse({'error': "Invalid Credentials, Please try again..."}, status=401)
        else:
            return JsonResponse({'error': "Incomplete login details"}, status=400)
        
        
    def get(self, request):
        # login_user_without_password(request, 'admin')

        if request.user.is_authenticated:
            return redirect('module_dashboard')
        
        logout(request)
        return render(request, 'auth/login.html')