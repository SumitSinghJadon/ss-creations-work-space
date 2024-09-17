from django.shortcuts import render, redirect
from django.views import View
from django.db import connections
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token 
from IS_Nexus.functions.data_conversion import queryset_to_json
from django.core import serializers
import json
from datetime import date
from django.core.serializers import serialize
from QMS_db.models.qms_planing import QmsPlaning
from QMS_db.models.swing_line_input import SewingLineInputMt,SewingLineInputDt


class SewingLineInputView(View):
    
    @method_decorator(csrf_exempt)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            plan_id = data.get('id',None)
            quantity = data.get('quantity')
            size = data.get('size')
            entry_time = data.get('entry_time')
            # entry_date = data.get('entry_date')
            entry_date = date.today().strftime('%m/%d/%Y')
            
            print ("data",data)
            existing_plan = QmsPlaning.objects.get(pk=plan_id)
            print("existing Plan",existing_plan)
            existing_data = SewingLineInputMt.objects.filter(
                planing__id=existing_plan.id,
                size = size
            ).first()
            print("existing_data",existing_data)
            
            if existing_data:
                prv_total_q = existing_data.total_input_qty
                existing_data.total_input_qty = quantity + prv_total_q
                existing_data.save()
                mt_data = existing_data
                
            else :
                mt_data = SewingLineInputMt.objects.create(
                    planing = existing_plan,
                    size = size,
                    total_input_qty = quantity
                )
                
            SewingLineInputDt.objects.create(
                mt_id= mt_data,
                input_qty= quantity,
                entry_date = entry_date,
                entry_time = entry_time
            )
            return JsonResponse({'message':"Data Saved"},safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
        

    def get_size_list(self, request):
        buyer_code = request.GET.get('buyer')
        our_ref_no = request.GET.get('ourref')
        style_no = request.GET.get('styleno')
        color = request.GET.get('color')
        print("buyer",buyer_code)
        cursor = connections['is_app_db'].cursor()
        # sql = '''
        #     EXEC GET_BUYER_COLOR_SIZE_QTY '{buyer_code}','{our_ref_no}','{style_no}','{color}';
        # '''
        sql = '''
            EXEC GET_BUYER_COLOR_SIZE_QTY %s, %s, %s, %s;
        '''
        cursor.execute(sql, (buyer_code, our_ref_no, style_no, color))
        size_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()
        return size_list or None
    
    
    @csrf_exempt
    def get(self, request):
        size_list = self.get_size_list(request)
        
        return JsonResponse(size_list, safe=False)
    
    
  


class SewingLineInputDtView(View):

    @method_decorator(csrf_exempt)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def get_today_size_by_id(self,request):
        id = request.GET.get('id')
        # print("id",id)
        plan_data = QmsPlaning.objects.get(id=id)
        entry_date = date.today()
        entry_date_str = entry_date.strftime('%m/%d/%Y')
        print(entry_date,"date",entry_date_str)
        
        exists_list = SewingLineInputMt.objects.filter(planing__id=plan_data.id)
        size_quantity_map = {}
        for exists in exists_list:
            size_dt_data = SewingLineInputDt.objects.filter(mt_id__id=exists.id,entry_date=entry_date_str)
            # print(size_dt_data)
            
            # print(size_dt_data)
            for item in size_dt_data:
                print(item.entry_date)
                size = exists.size
                quantity = item.input_qty
                if size in size_quantity_map:
                    size_quantity_map[size] += quantity
                else:
                    size_quantity_map[size] = quantity
        
        size_dt_list = [{'size': size, 'quantity': quantity} for size, quantity in size_quantity_map.items()]
        
        return size_dt_list
    
    def get_size_data(self,request):
        id = request.GET.get('id')
        plan_data = QmsPlaning.objects.get(id=id)
        entry_date = date.today()
        entry_date_str = entry_date.strftime('%m/%d/%Y')
        exists_list = SewingLineInputMt.objects.filter(planing__id=plan_data.id).values()
        
        return list(exists_list)
        
    
    @csrf_exempt
    def get(self, request):
        size_dt_list = self.get_today_size_by_id(request)
        size_mt_list = self.get_size_data(request)
        context={
            'size_dt_list':size_dt_list,
            'size_mt_list':size_mt_list
        }
        return JsonResponse(context, safe=False)
    
    
    
