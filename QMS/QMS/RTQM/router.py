from rest_framework import routers
from .views.ob_details import ExcelDataShowViewSet
router = routers.DefaultRouter()
router.register(r'ExcelDataShow', ExcelDataShowViewSet,basename="ExcelDataShow")   