from django.urls import path
from EntryForms.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('sample-booking/', login_required(SampleBookingDashboard.as_view()), name='sample_booking_page'),
    path('sample-booking/add/', login_required(SampleBookingView.as_view()), name='sample_booking_add_page'),
    path('sample-booking/print/', login_required(SamplePrintView.as_view()), name='sample_booking_print_page'),
    
    path('booking-confirmation/', login_required(BookingConfirmationDashboardView.as_view()), name='booking_confirmation_dashboard_page'), 
    path('booking-confirmation/add/', login_required(BookingConfirmationView.as_view()), name='booking_confirmation_page'), 
    
    path('pattern-request/',login_required(PatternRequestView.as_view()), name='pattern_request_page'),
    path('cutting-dashboard/', login_required(CuttingDashboardView.as_view()),name='cutting_Dashboard_page'),
    path('stitch-dashboard/', login_required(StitchDashboardView.as_view()),name='stitch_Dashboard_page'),
    path('cutting-entry/', login_required(CuttingEntryView.as_view()),name='cutting_entry_page'),
    path('stitching-transaction-entry/', login_required(StitchingEntryView.as_view()), name='stitching_transaction_entry_page'),
    path('checker-status/', login_required(CheckerStatusView.as_view()), name='checker_status_page'),
    path('finishing-transaction-entry/', login_required(FinishingTransactionEntryView.as_view()), name='finishing_transaction_entry_page'),
    path('size-wise-cut-qty/',login_required(SizeWiseCutQtyView.as_view()), name='size_wise_cut_qty_page'),
    path('size-wise-stitch-qty/',login_required(SizeWiseStitchQtyView.as_view()), name='size_wise_stitch_qty_page'),

    path('finishing-transaction-history/', login_required(FinishingTransactionHistoryView.as_view()), name='finishing_transaction_history_page'),
    path('stitching-defects/', login_required(StitchingDefectsView.as_view()), name='stitching_defects_page'),
    path('size-wise-finish-qty/', login_required(SizeWiseFinishQtyView.as_view()), name='Size_wise_finish_qty_page'),
    path('pattern-request-status/', login_required(PatternRequestStatusView.as_view()), name='pattern_request_status_page'), 
    path('sample-article-confirmation/', login_required(SampleArticleConfirmationView.as_view()), name='sample_article_confirmation_page'), 
    path('save-record/', login_required(SaveRecordView.as_view()), name='save_record_page'),

    path('finishing-defects/', login_required(finishingDefectsView.as_view()), name='finishing_defects_page'),
    path('finishing-dashboard/', login_required(finishDashboardView.as_view()),name='finish_Dashboard_page'),

    path('dispatch-transaction-entry/', login_required(DispatchTransactionEntryView.as_view()), name='dispatch_transaction_entry_page'),
    path('dispatch-defects/', login_required(DispatchDefectsView.as_view()), name='dispatch_defects_page'),
    path('dispatch-dashboard/', login_required(dispatchDashboardView.as_view()),name='dispatch_Dashboard_page'),

    path('trans-size/', login_required(TransactionSizeEntryView.as_view()),name='Transaction_size_entry_page'),
    path('wip/', login_required(SamplingWIPView.as_view()),name='Sampling_WIP_page'),
    path('cost_summ/', login_required(SamplingCostSummView.as_view()),name='Sampling_Cost_summary_page'),

    path('cost/', login_required(SamplingCostView.as_view()),name='Sampling_Cost_page'),
    path('day-cost/', login_required(DayCostView.as_view()),name='Sampling_Day_Cost_page'),
    path('eff/', login_required(TailorEffView.as_view()),name='Tailor_Eff_page'),
    path('day-eff/', login_required(DayEffView.as_view()),name='Tailor_Day_Eff_page'),
    path('sample-assign/', login_required(SampleAssignView.as_view()),name='Sample_Allocation_page'),
    path('sample-status/', login_required(SampleStatusView.as_view()),name='sample_status_page'),
    path('other-transaction-entry/', login_required(OtherEntryView.as_view()), name='other_transaction_entry_page'),
    path('other-dashboard/', login_required(OtherDashboardView.as_view()),name='other_entry_Dashboard_page'),

    path('trans/', login_required(SamplingTransView.as_view()),name='Sampling_WIP_page'),
    path('other-entry/', login_required(OtherTransView.as_view()), name='other_entry_page'),
    path('other-sample-booking/', login_required(OtherSampleBookingDashboard.as_view()), name='other_sample_booking_page'),
    path('other-sample-booking/add/', login_required(OtherTransView.as_view()), name='other_sample_booking_add_page'),
    path('sample-trans/', login_required(SampleTransReportView.as_view()),name='Sampling_Transaction_page'),
    path('send-mail/', SendMailView.as_view(), name='save_record_page'),
]

