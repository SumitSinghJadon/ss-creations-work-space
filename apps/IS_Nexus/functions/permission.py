from IS_Nexus.context.user_permission import user_permission
from django.core.handlers.wsgi import WSGIRequest


def get(request:WSGIRequest, ptype:str):
    if request.user.is_authenticated:
        data = user_permission(request)
        
        if ptype == 'page':
            permission = data['page_permission']

        elif ptype == 'page_list':
            permission = data['page_permission_list']

        elif ptype == 'module':
            permission = data['module_permission']

        elif ptype == 'module_list':
            permission = data['module_permission_list']

        elif ptype == 'page_id_list':
            permission = data['page_permission_id_list']

        elif ptype == 'location_list':
            permission = data['location_permission_list']

        elif ptype == 'location_pay_list':
            permission = data['location_permission_pay_list']
            
        else:
            permission = None
    else:
        permission = None

    return permission 


def location(request:WSGIRequest, ptype:str):
    if request.user.is_authenticated:
        data = user_permission(request)

