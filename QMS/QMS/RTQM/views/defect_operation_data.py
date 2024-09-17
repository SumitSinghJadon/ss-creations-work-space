from django.http import JsonResponse
from django.views import View
from QMS_db.models.defect_operation_data  import DefectOperationData
import json
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator

class DefectOperationDataView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        defect_operations = DefectOperationData.objects.filter(is_active=True)
        data = list(defect_operations.values())
        return JsonResponse(data, safe=False)
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_defect_operation = DefectOperationData(
            buyer=data['buyer'],
            ourref=data['ourref'],
            style=data['style'],
            color=data['color'],
            size=data['size'],
            defect_operation=data['defect_operation'],
            created_by=data['created_by']
        )
        new_defect_operation.save()
        return JsonResponse({'message': 'DefectOperationData created successfully'}, status=201)
