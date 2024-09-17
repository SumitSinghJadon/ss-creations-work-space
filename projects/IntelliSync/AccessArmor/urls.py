from django.urls import path
from AccessArmor.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(PermissionView.as_view()), name='permission_home_page'),
    path('user-permission/', login_required(UserPermissionView.as_view()), name='user_permission_page'),
    path('user-list/', login_required(UserList.as_view()), name='user_list_page'),
]

