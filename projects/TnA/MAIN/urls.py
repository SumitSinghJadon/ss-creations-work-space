from django.contrib import admin
from django.urls import path ,include
from AccessArmor.views import Dashboard 
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("IS_Nexus.urls")),
    path('dashboard/', login_required(Dashboard.as_view()), name='dashboard_page'),
    path('tna/',include("TnAMaster.urls")),
]

# if settings.DEBUG == True:
urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

