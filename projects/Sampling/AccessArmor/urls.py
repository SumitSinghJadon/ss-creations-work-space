from django.urls import path
from AccessArmor.views import *
from django.contrib.auth.decorators import login_required
from AccessArmor.views.test import Test


urlpatterns = [
    path('', login_required(PermissionView.as_view()), name='permission_home_page'),
    path('user-permission/', login_required(UserPermissionView.as_view()), name='user_permission_page'),
    path('test/', Test.as_view(), name='user_permission_page')
]

