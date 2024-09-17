from django.urls import path, include 
from django.contrib.auth.decorators import login_required 
from AccessArmor.views import Dashboard
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("IS_Nexus.urls")),
    path('access-armor/', include('AccessArmor.urls')),
    path('dashboard/', login_required(Dashboard.as_view()), name='dashboard_page'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('rtqm/', include('RTQM.urls')),
    path('masters/',include('Masters.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

