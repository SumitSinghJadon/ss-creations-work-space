from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
from QMS_db.models import DefectMaster ,ProcessMaster
import json
from django.shortcuts import get_object_or_404



class DefectMasterView(View):
    
    @method_decorator(csrf_exempt)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(request,self):
        try:
            defect_master = DefectMaster.objects.all().order_by('-id')
            dp_data = list(defect_master.values()) 
            process_data = list(ProcessMaster.objects.all().values())
            return JsonResponse({'dp_data': dp_data,'process_data':process_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
         
        
    
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        remarks = data.get('remarks')
        critical = data.get('critical')
        hindi_name = data.get('hindi_name')
        is_reject = data.get('is_reject')
        
        # print(data)
        process_id = data.get('process')
        process_instance = get_object_or_404(ProcessMaster, id=process_id)
        
        if name is not None and remarks is not None:
            defect_master = DefectMaster.objects.create(name=name, remarks=remarks,critical=critical,hindi_name=hindi_name,process=process_instance,is_reject=is_reject)
            return JsonResponse({'message': 'DefectMaster created successfully', 'id': defect_master.id}, status=201)
        else:
            return JsonResponse({'error': 'Name or status is missing'}, status=400)