from django.urls import path,include

from .views.api import RtqmAPI

from .views.rtqm import RtqmDtMtView, RtqmDtView,RtqmMtDtPassView, RtqmMtDtRectifiedView
from .views.order_process_plan import OrderProcessPlan
from .views import SendToQMS, RTQMView, UploadOB
from .views.send_to_qms import * 
from .views.order_dt_views import *
from .views.qms_planing import *
from .views.qms_tab_login import *
from .views.qms_defect_process import *
from .views.home import Home
# from .router import *
from .views.ob_details import ExcelDataShowView, ObDetailsView, ObMasterView
from .views.sewing_line_input import SewingLineInputDtView,  SewingLineInputView


from .views.sewing_tv_dashboard import SewingTvDashboard, SewingTvDashboard2
urlpatterns = [
    # path('qms/', include(router.urls)),
    path('', RTQMView.as_view(), name='rtqm_page'),
    path("send_to_qms/", SendToQMS.as_view(), name='Send_To_QMS'),
    path("send_to_qms2/", SendToQMS2.as_view(), name='Send_To_QMS2'), 
    path("order_dt_view/", OrderDtView.as_view(), name='order_dt_view'),
    path("order_dt_view2/", OrderDtView2.as_view(), name='order_dt_view2'),
    path('order_process_plan/', OrderProcessPlan.as_view(), name='order_process_plan'),
    path('upload_ob/', UploadOB.as_view(), name='upload_ob_page'),
    path("qms_planing/",QmsPlaningView.as_view(),name='qms_planing'),
    path("qms_planing2/",QmsPlaningView2.as_view(),name='qms_planing2'),
    path("qms_tab_login/",QmsTabLogin.as_view(),name='qms-tab-login'),
    path("qms_defect_process/",QmsDefectView.as_view(),name='qms-defect-process'),
    path("home/",Home.as_view(),name='home'),
    path("excel_data_show_view/",ExcelDataShowView.as_view(),name="ExcelDataShowView"),
    path("style_silhouettes/",StyleSilhouettesView.as_view(),name="style-silhouettes"),
    path("sewing_line_input/",SewingLineInputView.as_view(),name="sewing-line-input"),
    path("sewing_line_dt_input/",SewingLineInputDtView.as_view(),name="sewing-line-dt-input"),
    path('ob_details_view/',ObDetailsView.as_view(),name="ob-details-view"),
    path('rtqm_dt_mt_view/',RtqmDtMtView.as_view(),name="rtqm-dt-mt-view"),
    path('rtqm_dt_mt_pass_view/',RtqmMtDtPassView.as_view(),name="rtqm-dt-mt-pass-view"),
    path('rtqm_dt_mt_rectified_view/',RtqmMtDtRectifiedView.as_view(),name="rtqm-dt-mt-rectified-view"),
    path('ob_mt_data/',ObMasterView.as_view(),name="ob-mt-data"),
    path('rtqm_api/',RtqmAPI.as_view(),name='rtqm-api'),
    path('silhouettes_view/',SilhouettesView.as_view(),name='silhouettes-view'),
    path('rtqm_dt_view/',RtqmDtView.as_view(),name='rtqm-dt-view'),
    path('sewing_tv_dashboard/',SewingTvDashboard.as_view(),name='sewing-tv-dashboard'),
    path('sewing_tv_dashboard2/',SewingTvDashboard2.as_view(),name='sewing-tv-dashboard2'),
    
    
    
    
    
    
    

]
