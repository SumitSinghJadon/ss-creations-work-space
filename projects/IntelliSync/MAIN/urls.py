from django.contrib import admin 
from django.urls import path, include 
from django.contrib.auth.decorators import login_required 
from AccessArmor.views import Dashboard 

from Client.views import ReportingPerson
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("IS_Nexus.urls")),
    path('masters/', include('Masters.urls')),
    path('access-armor/', include('AccessArmor.urls')),
    path('clients/', login_required(ReportingPerson.as_view()),name="reporting_manager"),
    path('dashboard/', login_required(Dashboard.as_view()), name='dashboard_page'),
    # If debug == True
    path("__debug__/", include("debug_toolbar.urls")),
]

# urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
