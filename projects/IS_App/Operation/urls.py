from django.urls import path, include 
from django.contrib.auth.decorators import login_required


from .views import *
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'FileHandOverViewSet', FileHandOverViewSet,basename="FileHandOverViewSet")   

urlpatterns = [
    path('product/', FileHandOverView.as_view(), name='production_page'),
    path('product/filter/', BuyerFilterView.as_view(), name='production_page'),
    path('product/stylefilter/', StyleFilterView.as_view(), name='production_page'),
]

urlpatterns += router.urls