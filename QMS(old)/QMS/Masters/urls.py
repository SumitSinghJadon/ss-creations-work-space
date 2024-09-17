from django.urls import path
from .views.defect_master import *
from .views.qms_login import *
urlpatterns = [
    path('defect_master/',DefectMasterView.as_view(),name="defect-master"),
    path('master_login/',LoginView.as_view(),name="master-login")
    
    
]
