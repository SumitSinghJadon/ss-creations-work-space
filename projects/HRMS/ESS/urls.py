from django.urls import path
from ESS.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('daily-attendance/', login_required(DailyAttendanceView.as_view()), name='daily_attendance_page'),
    path('leave-application/', login_required(LeaveView.as_view()), name='leave_application_form_page'),
    path('od-application/', login_required(ODView.as_view()), name='od_application_form_page'),
    path('comp-off-application/', login_required(CompOffView.as_view()), name='Comp-Off_application_form_page'),
    path('miss-punch-application/', login_required(MissPunchView.as_view()), name='miss_punch_application_form_page'),
    path('wfh-application/', login_required(WfhView.as_view()), name='WFH_application_form_page'),
    path('application-approval/', login_required(ApplicationListView.as_view()), name='application_approval_page'),
    path('get/leave/details/',login_required(LeaveApplicationDetails.as_view())),
    path('application-report/',login_required(ApplicationReport.as_view()),name="application_report_page"),
    path('payslip-generate/',login_required(PayslipGenerator.as_view()),name="payslip_generator_page"),
    path('book-meeting-room/',login_required(MeetingBookingView.as_view()),name="book_meeting_room_page"),
    path('daily-application-mail/',ApplicationReport.as_view()),
    path('approve-over-mail/',ApprovalOverMail.as_view()),
    path('reject-over-mail/',RejectOverMail.as_view()),
    path('happy-bday/',HappyBdayMailer.as_view()),
    path('team-attendance/',TeamAttendanceView.as_view(),name='team_attendance_page'),
    path('generate-id-card/',GenerateIdCardView.as_view(),name='generate_id_card_page')
]

