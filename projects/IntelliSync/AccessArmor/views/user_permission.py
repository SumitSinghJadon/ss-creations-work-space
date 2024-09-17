from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import User, PagePermissionMaster, MenuMaster, UserPermissionMaster, ModuleMaster, LocationMaster, LocationPermission
from IS_Nexus.functions import messages
from Payroll_db.models import EmployeeMaster
from django.db.models import Q
from django.contrib import messages as alert
from IS_Nexus.functions.shortcuts import get_or_none
from django.db.models.functions import Trim


class UserPermissionView(View):
    def get(self, request):
        """ Send data for filter """
        employee_list = (EmployeeMaster.objects.filter(resign=0, cat_code=4)
            .annotate(emp_pay_code = Trim('emp_paycode'))
            .values('emp_pay_code', 'emp_name').using('payroll_db'))
        module_list = ModuleMaster.objects.filter(is_active=True)
        
        context = {
            'employee_list' : employee_list,
            'module_list' : module_list
        }

        """ Provide data according to the filter """

        module = request.GET.get("mid")
        user = request.GET.get("uid")

        if module and user:
            user = get_or_none(User, username=user)
            # Create permission table
            page_list = MenuMaster.objects.filter(url__isnull=False, module=module).prefetch_related('pagepermissionmaster_set__permission')
            reporting_manager_list = User.objects.filter(is_reporting_manager = True, is_active=True)
            location_list = LocationMaster.objects.filter(is_active=True) 

            location_permission_list = LocationPermission.objects.filter(user=user).values_list('location__id', flat=True)
            user_permission_list = UserPermissionMaster.objects.filter(user=user).values_list('permission', flat=True)
            
            if user:
                reporting_manager_list = reporting_manager_list.exclude(username = user.username)

            context.update({
                'page_list' : page_list,
                'location_list' : location_list,
                'reporting_manager_list' : reporting_manager_list,
                'user_permission_list' : user_permission_list,
                'location_permission_list' : location_permission_list,
                'user' : user
            })

        return render(request, 'user_permission.html', context)


    def post(self, request):
        emp_pay_code = request.GET.get('uid')
        module_code = request.GET.get('mid')
        
        if emp_pay_code and module_code:
            user = get_or_none(User, username=emp_pay_code)
            
            if not user:
                # create new user
                emp = EmployeeMaster.objects.filter(resign=0, cat_code=4, emp_paycode=emp_pay_code).values('emp_paycode', 'emp_name').using('payroll_db')
                if emp:
                    user = User.objects.create(
                        username = str(emp_pay_code).strip(),
                        password = str(emp_pay_code).strip(),
                        full_name = emp[0]['emp_name'],
                        is_superuser = False
                    )
                    if user:
                        alert.success(request, "User successfully Created")
                    else:
                        alert.error(request, 'Unable to create user.')
                else:
                    alert.error(request, 'Provided user not found in payroll')
            

            if user:
                # give user permission 
                permission_list = request.POST.getlist('page_permission')
                location_list = request.POST.getlist('location_permission')
                is_reporting_manager = request.POST.get('is_reporting_manager')
                email = request.POST.get('email')
                location = request.POST.get('location')
                reporting_manager = request.POST.get('reporting_manager')
                permissions = []
                locations   = []

                for pid in permission_list:
                    try:
                        # Check is permission valid or not, if valid put it in permissions list for bulk create
                        permission = PagePermissionMaster.objects.get(id=pid)
                        permissions.append(UserPermissionMaster(user=user, permission=permission))

                    except PagePermissionMaster.DoesNotExist:
                        messages.update_error(request)
                    
                for lid in location_list: 
                    try:
                        location = LocationMaster.objects.get(id=lid)
                        locations.append(LocationPermission(user=user, location=location))
                    
                    except LocationMaster.DoesNotExist:
                        messages.update_error(request)

                # Delete all previous permissions for the user in a single database hit
                UserPermissionMaster.objects.filter(user=user, permission__page__module=module_code).delete()
                LocationPermission.objects.filter(user=user).delete()

                # Bulk create the new permissions
                UserPermissionMaster.objects.bulk_create(permissions)
                LocationPermission.objects.bulk_create(locations)
                
                if is_reporting_manager:
                    user.is_reporting_manager = is_reporting_manager
                
                if email:
                    user.email = email
                
                if location:
                    user.location = location
                
                if reporting_manager:
                    reporting_manager = User.objects.get(id=reporting_manager)
                    user.reporting_manager = reporting_manager
                
                user.save()
                messages.saved(request)

        else:
            messages.form_error(request)

        return redirect('user_permission_page')

