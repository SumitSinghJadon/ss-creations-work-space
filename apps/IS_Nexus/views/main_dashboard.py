from django.views import View
from django.shortcuts import redirect, render
from IntelliSync_db.models import ModuleMaster
from django.conf import settings


class MainDashboard(View):
    def get(self, request):
        module_list = ModuleMaster.objects.filter(is_active=True)
        context = {
            'module_list' : module_list
        }
        return render(request, 'auth/main_dashboard.html', context)

    def post(self, request):
        return redirect('main-dashboard')


class ModuleDashboardRouter(View):
    def get(self, request):
        if settings.PROJECT_CODE == "intelli_sync":
            return redirect('module-dashboard/')
        return redirect('/dashboard/')

