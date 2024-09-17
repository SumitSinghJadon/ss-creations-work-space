from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('common-master/', login_required(CommonMasterView.as_view()), name='common_master_page'),
    path('first-level-master/', login_required(FirstLevelMasterView.as_view()), name='first_level_master_page'),
    path('second-level-master/', login_required(SecondLevelMasterView.as_view()), name='second_level_master_page'),
]
