from django.urls import path
from Miscellaneous.views import (ManpowerPlanning,ManpowerPlanning_hr,Mmr,
                                 Punchdata,Staff_worker,Staff_worker_attr,OtApproval_view,OtApproval_view_all,
                                 OtApproval_gm,Ot_Master_add,OtApproval_head,
                                 OtApproval_unauth,Daily_manpower_summ,CuttingReportView, FinishingReportView,
                                 ManpowerAllocationView ,SaveDataView,ManpowerAllocReportView
                                 )
from django.contrib.auth.decorators import login_required
from .views.turnover_view import SaleTurnoverView
from .views.buyer_claim_view import BuyerClaimView
from .views.buyer_claim_details import BuyerClaimDetailView
from .views.buyer_claim_edit_update import BuyerClaimEditUpdate
from .views.on_time_delivery_view import OnTimeDeliveryView
from .views.ECF_electricity import ECFElectricityView
from .views.energy_cost_from import EnergyCostView 
from .views.air_freight_form import AirFreightForm

urlpatterns =[
    path('mmr/', login_required(Mmr.as_view())),
    path('staffworker/', login_required(Staff_worker.as_view())),
    path('staffworkerattr/', login_required(Staff_worker_attr.as_view())),
    path('punch/', login_required(Punchdata.as_view())),
    path('daily_manp/', login_required(Daily_manpower_summ.as_view())),
    path('ot_add/', login_required(OtApproval_view.as_view()), name='ot_add_page'),
    path('ot_view/', login_required(OtApproval_view_all.as_view()), name='ot_view_page'),
    path('ot_master/', login_required(Ot_Master_add.as_view()), name='ot_master_page'),
    path('ot_head/', login_required(OtApproval_head.as_view()), name='ot_approve_head_page'),
    path('ot_gm/', login_required(OtApproval_gm.as_view()), name='ot_approve_gm_page'),
    path('ot_unauth/', login_required(OtApproval_unauth.as_view()), name='ot_unauthorize_page'),
    path('manpower_hr/', login_required(ManpowerPlanning_hr.as_view())),
    path('manpower/', login_required(ManpowerPlanning.as_view()), name='manpower_planning_page'),
    path('cutting-report/', login_required(CuttingReportView.as_view()), name='cutting_report_page'),
    path('finishing-report/', login_required(FinishingReportView.as_view()), name='finishing_report_page'),
    path('alloc/', login_required(ManpowerAllocationView.as_view()), name='manpower_allocation_page'),
    path('alloc_day/', login_required(ManpowerAllocReportView.as_view()), name='manpower_allocation_report_page'),
    path('save/', login_required(SaveDataView.as_view()), name='save_data_page'),
    path('turnover/',login_required(SaleTurnoverView.as_view()),name='turnover'),
    path('ontimedel/',login_required(OnTimeDeliveryView.as_view()),name='ontimedel'),
    path('buyerClaim/',login_required(BuyerClaimView.as_view()),name='buyerClaimEntry'),
    path('buyerClaimDetails/',login_required(BuyerClaimDetailView.as_view()),name='buyerClaimDetails'),
    path('buyerClaimEdit/<id>',login_required(BuyerClaimEditUpdate.as_view()),name='buyerClaimEdit'),
    path('energyCost',login_required(EnergyCostView.as_view()),name='energy_cost_form'),
    path('electricityCost',login_required(ECFElectricityView.as_view()),name='Electricity_Cost_Form'),
    path('airFreightForm',login_required(AirFreightForm.as_view()),name='airFreight'),
]