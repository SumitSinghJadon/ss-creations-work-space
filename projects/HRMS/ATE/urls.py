from django.urls import path
from ATE.views import ManpowerRequisitionView, ManpowerStatusTracker
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('manpower-requisition/',login_required(ManpowerRequisitionView.as_view()),name="manpower_requisition_form_page"),
    path('manpower-status-tracker/',login_required(ManpowerStatusTracker.as_view()),name="manpower_status_tracker_page")
]

