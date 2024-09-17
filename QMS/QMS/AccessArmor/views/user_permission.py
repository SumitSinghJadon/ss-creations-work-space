from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import User, PagePermissionMaster, SubMenuMaster, UserPermissionMaster, PermissionMaster, ModuleMaster
from IS_Nexus.functions import messages
from django.db import transaction
from django.db.models import Count
from Payroll_db.models import EmployeeMaster
from IntelliSync_db.models import LocationMaster 


class UserPermissionView(View):
    def get(self, request):
        module = request.GET.get("mid")
        user = request.GET.get("uid")
        location_list = LocationMaster.objects.filter(is_active=True).values('id', 'name')
        employee_list = EmployeeMaster.objects.filter(resign=0, cat_code=4).values('emp_paycode', 'emp_name').using('payroll_db')

        if user and module:
            user = request.user

            page_list = SubMenuMaster.objects.select_related('main_menu').prefetch_related('pagepermissionmaster_set__permission')
            user_permissions = UserPermissionMaster.objects.filter(user=user).values_list('permission', flat=True)
            user_list = User.objects.filter(is_active=True)
            module_list = ModuleMaster.objects.filter(is_active=True)

            permissions_dict = (
                PermissionMaster.objects.annotate(num_pages=Count('pagepermissionmaster'))
                .filter(pagepermissionmaster__userpermissionmaster__user=user)
                .in_bulk(field_name='id')
            )

            context = {
                'module_list' : module_list,
                'page_list': page_list,
                'user_permissions': user_permissions,
                'permissions_dict': permissions_dict,
                'user_list' : user_list,
            }

        else:
            module_list = ModuleMaster.objects.filter(is_active=True)
            user_list = User.objects.filter(is_active=True)

            context = {
                'module_list' : module_list,
                'user_list' : user_list,
            }

        context['employee_list'] = employee_list
        context['location_list'] = location_list

        return render(request, 'user_permission.html', context)


    def post(self, request):
        permission_dict = request.POST.dict()
        user = request.user
        del permission_dict['csrfmiddlewaretoken']

        permissions = []
        
        for permission_id in permission_dict.values():
            try:
                permission = PagePermissionMaster.objects.get(id=permission_id)
                permissions.append(UserPermissionMaster(user=user, permission=permission))
                
            except PagePermissionMaster.DoesNotExist:
                messages.update_error(request)

        with transaction.atomic():
            # Delete all previous permissions for the user in a single database hit
            UserPermissionMaster.objects.filter(user=user).delete()

            # Bulk create the new permissions
            UserPermissionMaster.objects.bulk_create(permissions)

        messages.saved(request)
        return redirect('user_permission_page')

