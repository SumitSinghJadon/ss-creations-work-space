
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

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


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
        

class PPMsave(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        data = json.loads(request.body)
        print("Received data:", data)
        
        buyer = data.get('buyer')
        style = data.get('style')
        ourref = data.get('ourref')  # This might be None if not provided
        color = data.get('color')      # This might be None if not provided
        date = data.get('date')
        location = data.get('location')
        plan_data = data.get('planData')
        
        
        filter_criteria = {
            'buyer_code': buyer,
            'style_no': style,
        }
               
        if ourref is not None:
            filter_criteria['order_no'] = ourref
        else:
            filter_criteria['order_no__isnull'] = True
            
        # Include color only if it is provided
        if color is not None:
            filter_criteria['color'] = color
        else:
            filter_criteria['color__isnull'] = True 
        
        
        # Check if ProdProcPlanMt exists
        ppm_mt_exists = ProdProcPlanMt.objects.filter(**filter_criteria).exists()
        
        
        if not ppm_mt_exists:
            location = LocationMaster.objects.get(id=data['location'])
            print("Location:", location)
            new_number = get_next_number("PPPM")
            # Create a new ProdProcPlanMt object
            ProdProcPlanMt.objects.create(
                plan_no=new_number,
                buyer_code=buyer,
                style_no=style,
                order_no=ourref,
                color=color,
                u_id=location,
                entry_date=date
            )
            
        filter_criteria = {
            'buyer_code': buyer,
            'style_no': style,
        }
               
        if ourref is not None:
            filter_criteria['order_no'] = ourref
        else:
            filter_criteria['order_no__isnull'] = True
            
        # Include color only if it is provided
        if color is not None:
            filter_criteria['color'] = color
        else:
            filter_criteria['color__isnull'] = True 

        # Retrieve the ProdProcPlanMt object
        obj = ProdProcPlanMt.objects.get(**filter_criteria)
        
        print("ProdProcPlanMt object:", obj)

        # Check for duplicate process_id in planData
        for plan_data in data['planData']:
            process_id = plan_data['process_id']
            process_no = plan_data['process_no']
            
            # Check if a record with the same process_id already exists for this mt object
            exists = ProdProcPlanDt.objects.filter(
                mt=obj,
                process_id=process_id,
                active=True
                
            ).exists()
            
            check_process_no = ProdProcPlanDt.objects.filter(
                mt=obj,
                process_no=process_no,
                active=True
            ).exists()
            
            

            if exists:
                try:
                    process_instance = ProdProcPlanDt.objects.get(mt=obj,process_id=process_id ,active=True)
                    process_name = process_instance.process.name  # Assuming 'name' is the field containing the descriptive name
                except ProdProcPlanDt.DoesNotExist:
                    process_name = "Unknown Process"
                return JsonResponse({'error': f"{process_name} Already exists"}, status=400)
            
            if check_process_no:
                try:
                    process_instance = ProdProcPlanDt.objects.get(mt=obj,process_no=process_no ,active=True)
                    process_name = process_instance.process_no  # Assuming 'name' is the field containing the descriptive name
                except ProdProcPlanDt.DoesNotExist:
                    process_name = "Unknown Process"
                return JsonResponse({'error': f"{process_name} Process No  Already Exists"}, status=400)
            
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
            color = request.GET.get('color')  # Include color parameter
            date = request.GET.get('date')

            # Create a filter dictionary
            filter_args = {}
            
            if buyer:
                filter_args['buyer_code'] = buyer
            if style:
                filter_args['style_no'] = style
            if ourref:
                filter_args['order_no'] = ourref
            if color:  # Only include if color is provided
                filter_args['color'] = color
            # if date:  # Uncomment if you want to filter by date
            #     filter_args['entry_date'] = date

            # Filter the queryset based on provided parameters
            if buyer and style and color:
                queryset = ProdProcPlanMt.objects.filter(buyer_code=buyer, style_no=style, order_no__isnull=True, color=color)
            elif buyer and style and ourref:
                # Filter only by buyer, style, and order_no
                queryset = ProdProcPlanMt.objects.filter(buyer_code=buyer, style_no=style, order_no=ourref , color__isnull=True)
            elif buyer and style:
                # Filter only by buyer and style
                queryset = ProdProcPlanMt.objects.filter(buyer_code=buyer, style_no=style ,order_no__isnull=True, color__isnull=True) 

            # Extract IDs from the queryset
            ids = queryset.values_list('id', flat=True)
                
            print("ids",ids)

            if not ids:
                return JsonResponse({'error': 'No matching ProdProcPlanMt entries found'}, status=404)

            # Retrieve related ProdProcPlanDt entries using the IDs
            dt_queryset = ProdProcPlanDt.objects.filter(mt__in=ids ,active=True)
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
        
            
class ProcessDelete(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        id = json.loads(request.body)
        item = ProdProcPlanDt.objects.get(id=id)
       # Update the active status to False
        item.active = False
        item.save()
        return JsonResponse({'message': 'Item deleted successfully'}, status=200)
    
    
    

class ProcessUpdate(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)     
            id = data.get('id')
            # Retrieve the item by ID
            item = ProdProcPlanDt.objects.get(id=id)
            # Update fields with new data
            item.process_no = data.get('process_no', item.process_no)
            item.process_rate = data.get('process_rate', item.process_rate)
            item.product_rate = data.get('product_rate', item.product_rate)
            item.save()

            # Return success response with updated data
            return JsonResponse({'message': 'update successfully'}, status=200)
        except ProdProcPlanDt.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        


            
  

class InputsPPMshow(View):
    def get(self, request):
         # Extract query parameters
            buyer = request.GET.get('buyer')
            style = request.GET.get('style')
            ourref = request.GET.get('ourref')
            color = request.GET.get('color')  # Include color parameter
            date = request.GET.get('date')

            # Create a filter dictionary
            filter_args = {}
            
            if buyer:
                filter_args['buyer_code'] = buyer
            if style:
                filter_args['style_no'] = style
            if ourref:
                filter_args['order_no'] = ourref
            if color:  # Only include if color is provided
                filter_args['color'] = color
            # if date:  # Uncomment if you want to filter by date
            #     filter_args['entry_date'] = date

            # Filter the queryset based on provided parameters
            if buyer and style and color:
                queryset = ProdProcPlanMt.objects.filter(buyer_code=buyer, style_no=style, order_no__isnull=True, color=color)
            elif buyer and style and ourref:
                # Filter only by buyer, style, and order_no
                queryset = ProdProcPlanMt.objects.filter(buyer_code=buyer, style_no=style, order_no=ourref , color__isnull=True)
            elif buyer and style:
                # Filter only by buyer and style
                queryset = ProdProcPlanMt.objects.filter(buyer_code=buyer, style_no=style ,order_no__isnull=True, color__isnull=True) 

            # Extract IDs from the queryset
            ids = queryset.values_list('id', flat=True)
                
            print("ids",ids)

            if not ids:
                return JsonResponse({'error': 'No matching ProdProcPlanMt entries found'}, status=404)

            # Retrieve related ProdProcPlanDt entries using the IDs
            dt_queryset = ProdProcPlanDt.objects.filter(mt__in=ids ,active=True)
            
                # Serialize the queryset
            serialized_dt_data = list(dt_queryset.values()) 

       
            
            print("serialized_dt_data",serialized_dt_data)
            # Combine and return data
            combined_data = {
                'prod_proc_plan_dt': serialized_dt_data
            }
            return JsonResponse(combined_data, safe=False)   