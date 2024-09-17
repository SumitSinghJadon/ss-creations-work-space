from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import ModuleMaster
from IS_Nexus.functions import permission
from django.db.models import F 
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from IntelliSync_db.models import User 


class ModuleDashboard(View):
    def get(self,request):
        module_permission = permission.get(request, 'module_list')
        module_items = ModuleMaster.objects.filter(is_active=True, id__in=module_permission).annotate(
            server_ip = F('project__company__server_ip'),
            port_no = F('project__server_port'),
        ).values('name', 'image', 'server_ip', 'port_no', 'dashboard_url')
        
        context = {
            'host' : request.get_host().split(':')[0],
            'module_list' : module_items
        }

        return render(request, 'auth/module_dashboard.html', context)


    def post(self, request):
        User = get_user_model()
        user = request.user
        
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        if user.check_password(old_password): 
            user = User.objects.get(username = user.username)
            user.password = new_password
            user.save()
            messages.warning(request, 'Password Change, Login again with new password.')
        
        else:
            messages.error(request, "Incorrect old password")

        return redirect('module_dashboard')

