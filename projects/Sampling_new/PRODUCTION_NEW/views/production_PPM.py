
from django.db import connections
from django.views import View
from  django.http import JsonResponse
from IntelliSync_db.models import CommonMaster
from IntelliSync_db.models import FirstLevelMaster,SecondLevelMaster
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
import json
from IS_erp_db.models.production_mt.prod_proc_plan_mt import ProdProcPlanMt
from IS_erp_db.models.production_dt.prod_proc_plan_dt import ProdProcPlanDt
from ERP_db.models.part import Party
from IntelliSync_db.models.is_settings.numbering_method import get_next_number
from IntelliSync_db.models.location_master import LocationMaster
from IntelliSync_db.models import CommonMaster
from IntelliSync_db.models import FirstLevelMaster,SecondLevelMaster

class ProcessView(View):
        def get(self, request):
            process = FirstLevelMaster.objects.filter(master_type__code='CT-8', is_active=True).using('intellisync_db').values('id', 'name')    
            process_list = list(process)
            print(process_list)  
            return JsonResponse({'data': process_list}, safe=False)
        
class ComponentView(View):
        def get(self, request):
            component = FirstLevelMaster.objects.filter(master_type__code='CT-9', is_active=True).using('intellisync_db').values('id', 'name')
            component_list = list(component)
            print(component_list)
            return JsonResponse({'data': component_list}, safe=False)
        
class SubComponentView(View):
        def get(self, request):
            Component_id = request.GET.get('component_id')
            sub_component = SecondLevelMaster.objects.filter(master_type__code='CT-10', first_level_master = Component_id , is_active=True).using('intellisync_db').values('id', 'name')
            sub_component_list = list(sub_component)
            print(sub_component_list)
            return JsonResponse({'data': sub_component_list}, safe=False)
        
        
class Product(View):
        def get(self, request):
            Product = CommonMaster.objects.filter(master_type__code='CT-7', is_active=True).using('intellisync_db').values('id', 'name')
            Product_list = list(Product)
            print(Product_list)
            return JsonResponse({'data': Product_list}, safe=False)
        
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

class PPMsave(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        data = json.loads(request.body)
        print("Received data:", data)
        # Check if ProdProcPlanMt exists
        ppm_mt_exists = ProdProcPlanMt.objects.filter(
            buyer_code=data['buyer'],
            style_no=data['style'],
            order_no=data['ourref']
        ).exists()

        if not ppm_mt_exists:
            location = LocationMaster.objects.get(id=data['location'])
            print("Location:", location)
            new_number = get_next_number("PPPM")
            ProdProcPlanMt.objects.create(
                plan_no=new_number,
                buyer_code=data['buyer'],
                style_no=data['style'],
                order_no=data['ourref'],
                u_id=location,
                entry_date=data['date']
            )

        # Retrieve the ProdProcPlanMt object
        obj = ProdProcPlanMt.objects.get(
            buyer_code=data['buyer'],
            style_no=data['style'],
            order_no=data['ourref']
        )

        # Check for duplicate process_id in planData
        for plan_data in data['planData']:
            process_id = plan_data['process_id']
            # Check if a record with the same process_id already exists for this mt object
            exists = ProdProcPlanDt.objects.filter(
                mt=obj,
                process_id=process_id
            ).exists()

            if exists:
                try:
                    process_instance = ProdProcPlanDt.objects.get(mt=obj,process_id=process_id)
                    process_name = process_instance.process.name  # Assuming 'name' is the field containing the descriptive name
                except ProdProcPlanDt.DoesNotExist:
                    process_name = "Unknown Process"
                return JsonResponse({'error': f"{process_name} Already exists"}, status=400)
        # Create ProdProcPlanDt entries
        for plan_data in data['planData']:
            process_instance = FirstLevelMaster.objects.get(id=plan_data['process_id'])
            product_type_ins = CommonMaster.objects.get(id=plan_data['product_type_id'])
            component_ins = FirstLevelMaster.objects.get(id=plan_data['component_id'])
            sub_component_ins = SecondLevelMaster.objects.get(id=plan_data['sub_component_id'])
            ProdProcPlanDt.objects.create(
                mt=obj,
                plan_no=obj.plan_no,
                process=process_instance,
                product_type=product_type_ins,
                component=component_ins,
                sub_component=sub_component_ins,
                process_no=plan_data['process_no'],
                process_rate=plan_data['process_rate'],
                product_rate=plan_data['product_rate'],
            )

        return JsonResponse({'data': "success"}, safe=False)


class PPMshow(View):
    def get(self, request):
        # Extract query parameters
        buyer = request.GET.get('buyer')
        style = request.GET.get('style')
        ourref = request.GET.get('ourref')
        date = request.GET.get('date')

        # Check for required parameters
        if buyer and style and ourref:
            # Filter the queryset based on provided parameters
            queryset = ProdProcPlanMt.objects.filter(
                buyer_code=buyer,
                style_no=style,
                order_no=ourref,
                # entry_date=date
            )

            # Extract IDs from the queryset
            ids = queryset.values_list('id', flat=True)
            
            print("ids",ids)

            if not ids:
                return JsonResponse({'error': 'No matching ProdProcPlanMt entries found'}, status=404)

            # Retrieve related ProdProcPlanDt entries using the IDs
            dt_queryset = ProdProcPlanDt.objects.filter(mt__in=ids)
            serialized_dt_data = []
            for item in dt_queryset:
                data = {
                    'id': item.id,
                    'plan_no': item.plan_no,
                    'process': item.process.name if item.process else None,  # Example: ForeignKey field `process`
                    'product_type': item.product_type.name if item.product_type else None,  # Example: ForeignKey field `product_type`
                    'component': item.component.name if item.component else None,  # Example: ForeignKey field `component`
                    'sub_component': item.sub_component.name if item.sub_component else None,  # Example: ForeignKey field `sub_component`
                    'process_no': item.process_no,
                    'process_rate': item.process_rate,
                    'product_rate': item.product_rate,
                    'entry_status': item.entry_status,
                    'active': item.active,
                    'deleted': item.deleted,
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                }
                serialized_dt_data.append(data)
            
            print("serialized_dt_data",serialized_dt_data)

            # Combine and return data
            combined_data = {
                'prod_proc_plan_dt': serialized_dt_data
            }

            return JsonResponse(combined_data, safe=False)
        else:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        
class ProcessDelete(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        id = json.loads(request.body)
        item = ProdProcPlanDt.objects.get(id=id)
        item.delete()

        return JsonResponse({'message': 'Item deleted successfully'}, status=200)