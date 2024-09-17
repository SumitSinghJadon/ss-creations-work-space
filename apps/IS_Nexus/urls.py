from django.urls import path
from IS_Nexus.views import LoginView, MainDashboard, logout_user, ModuleDashboard, UserProfile, Restricted, login_user_without_password
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(ModuleDashboard.as_view()), name='module_dashboard'),
    path('restricted/', Restricted.as_view()),
    path('login/', LoginView.as_view(), name='login_page'),
    path('knox-login/', login_user_without_password, name='knox_login_page'),
    path('logout/', logout_user, name='logout_page'),
    path('user-profile/', login_required(UserProfile.as_view()), name='logout_page'),
]
