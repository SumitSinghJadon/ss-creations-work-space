from django.views import View
from QMS_db.models import SewingPlanning
from django.http import JsonResponse
from IntelliSync_db.models import LocationMaster, FirstLevelMaster


def get_unit(request):
    # Query SewingPlanning from the default database
    unit_ids = SewingPlanning.objects.filter(
        is_closed=False, is_active=True
    ).values_list('unit__id', flat=True).distinct()
    unit_list = LocationMaster.objects.filter(id__in = list(unit_ids)).values('name', 'id').using('intellisync_db')
    data = list(unit_list)
    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})


def get_line_by_unit(request):
    unit_id = request.GET.get('unit_id')

    if not unit_id:
        return JsonResponse({'error': 'unit_id parameter is required'}, status=400)
    
    line_ids = SewingPlanning.objects.filter(
        is_closed=False, is_active=True, unit=unit_id
    ).values_list('unit__id', flat=True).distinct()
    line_list = FirstLevelMaster.objects.filter(id__in = list(line_ids)).values('name', 'id').using('intellisync_db')
    data = list(line_list)
    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})


def get_planning_data_by_line(request):
    line_id = request.GET.get('line_id')
    
    if not line_id:
        return JsonResponse({'error': 'line_id parameter is required'}, status=400)

    line_list = SewingPlanning.objects.filter(
        is_closed=False, is_active=True, line=line_id
    ).values(
        'buyer', 'buyer_name', 'style_no', 'color', 'ourref', 'delvdate', 'quantity', 'planning_no', 'planning_date'
    ).distinct()
    
    data = list(line_list)  # Convert the queryset to a list of dictionaries
    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})

