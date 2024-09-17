from django.urls import path 
from .views import CuttingTransactionView
from .views.sample_assign import SampleAssignView


urlpatterns = [
    path('cutting-transaction/', CuttingTransactionView.as_view(), name="cutting_transaction_view_page"),
    path('sample_assign/',SampleAssignView.as_view(),name='sample_assign')

]
