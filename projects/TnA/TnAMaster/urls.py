from django.urls import path
from TnAMaster.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('tna_template/', login_required(TnaTemplateHistoryView.as_view()),name='T&A_Template_History_page'),
    path('tna_template/add/', login_required(TnaTemplateView.as_view()), name='T&A_Template_page'),

]