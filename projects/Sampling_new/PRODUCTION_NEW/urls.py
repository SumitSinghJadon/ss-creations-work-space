
from django.contrib.auth.decorators import login_required
from .views.production_login import *
from .views.production_all_get_data import *
from .views.production_PPM import *

from rest_framework import routers
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('unit/', LoginUnit.as_view(), name='unit'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('buyer/', BuyerFilterView.as_view(), name='buyer'),
    path('style/', StyleFilterView.as_view(), name='style'),
    path('ourref/', OurRefFilterView.as_view(), name='ourref'),
    path('color/', ColorFilterView.as_view(), name='color'),
    path('process/', ProcessView.as_view(), name='process'),
    path('component/', ComponentView.as_view(), name='component'),
    path('subcomp/', SubComponentView.as_view(), name='subcomp'),
    path('product/',Product.as_view(), name='product'),
    path('ppm/', PPMsave.as_view(), name='ppm'),
    path('ppmShow/', PPMshow.as_view(), name='ppmShow'),  
    path('ppmDelete/', ProcessDelete.as_view(), name='ppmDelete'),
    path('ppmUpdate/', ProcessUpdate.as_view(), name='ppmUpdate'),
    path('ppmInputs/', InputsPPMshow.as_view(), name='ppmInputs'),
]

