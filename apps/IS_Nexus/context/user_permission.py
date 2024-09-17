from IntelliSync_db.models import UserPermissionMaster, PagePermissionMaster, ModuleMaster, MenuMaster, LocationPermission
from django.core.handlers.wsgi import WSGIRequest


def superuser_permission():
    page_permission_list = PagePermissionMaster.objects.filter(is_active=True).values_list('permission__code', flat=True).distinct()
    module_permission_list = ModuleMaster.objects.filter(is_active=True).values_list('id', flat=True).distinct()
    page_permission_id_list = MenuMaster.objects.filter(is_active=True).values_list('id', flat=True).distinct()
    location_permission_list = LocationPermission.objects.all().values_list('location' ,flat=True).distinct()
    location_permission_pay_list = LocationPermission.objects.all().values_list('location__payroll_code' ,flat=True).distinct()
    
    return {
        'page_permission_list' : page_permission_list,
        'page_permission' : ''.join(perm for perm in  page_permission_list),
        'module_permission_list' : module_permission_list,
        'module_permission' : ''.join(str(perm) for perm in module_permission_list),
        'page_permission_id_list' : page_permission_id_list,
        'location_permission_list' : location_permission_list,
        'location_permission_pay_list' : location_permission_pay_list
    }


def user_permission(request:WSGIRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return superuser_permission()

        current_url = request.path
        user = request.user
        page_permission_list = UserPermissionMaster.objects.filter(
                user=user, permission__page__url = current_url, permission__is_active=True
            ).values_list('permission__permission__code', flat=True).distinct()
        
        page_permission_id_list = UserPermissionMaster.objects.filter(
                user=user, permission__is_active=True
            ).values_list('permission__page__id', flat=True).distinct()
        
        module_permission_list = UserPermissionMaster.objects.filter(
            user=user, permission__is_active=True
        ).values_list('permission__page__module__id', flat=True).distinct()

        
        location_permission_list = LocationPermission.objects.filter(user = user).values_list('location' ,flat=True).distinct()

        location_permission_pay_list = LocationPermission.objects.filter(user = user).values_list('location__payroll_code' ,flat=True).distinct()

        return {
            'page_permission_list' : page_permission_list,
            'page_permission' : ''.join(perm for perm in  page_permission_list),
            'module_permission_list' : module_permission_list,
            'module_permission' : ''.join(str(perm) for perm in module_permission_list),
            'page_permission_id_list' : page_permission_id_list,
            'location_permission_list' : location_permission_list,
            'location_permission_pay_list' : location_permission_pay_list
        }
    return {}


def user_permission_value(request:WSGIRequest):
    if request.user.is_authenticated:
        data = user_permission(request)
        page_permission = data['page_permission']
        page_permission_list = data['page_permission_list']
        module_permission = data['module_permission']
        module_permission_list = data['module_permission_list']
        return page_permission, page_permission_list, module_permission, module_permission_list 

    return {}



