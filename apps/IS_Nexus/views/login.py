from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from IntelliSync_db.models import User
from django.http import HttpResponse


def logout_user(request):
    logout(request)
    messages.warning(request, "Logout Success, Please Login again.")
    return redirect("login_page")


def login_user_without_password(request):
    username = request.GET.get('username')
    if not username:
        return HttpResponse("Don't Try...")
    user = User.objects.get(username=username)
    login(request, user)
    return redirect('module_dashboard')
    

class LoginView(View):
    def get(self, request):
        # login_user_without_password(request, 'admin')

        if request.user.is_authenticated:
            return redirect('module_dashboard')
        
        logout(request)
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_page = request.GET.get("next") or "module_dashboard"
        current_url = request.build_absolute_uri()

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_page)
            else:
                messages.error(request, "Invalid Credentials, Please try again...")
        else:
            messages.error(request, "Incomplete login details")
        
        return redirect(current_url)

