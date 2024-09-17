from django.shortcuts import render, redirect
from django.views import View
from django.db import connections
from django.http import JsonResponse
from QMS_db.models import SwingLineInputMt
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token 
from IS_Nexus.functions.data_conversion import queryset_to_json
from django.core import serializers
import json
from datetime import datetime
from django.core.serializers import serialize
from QMS_db.models.sewing_planning import SewingPlanning
from QMS_db.models.swing_line_input import SwingLineInputDt


class SewingLineInputView(View):
    @method_decorator(csrf_exempt)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



    def post(self, request):
        try:
            data = json.loads(request.body)
            plan_id = data.get('plan_id',None)

            existing_plan = SewingPlanning.objects.get(pk=plan_id)

            existing_data = SwingLineInputMt.objects.filter(
                planing__id=existing_plan.id,
            ).first()
            
            if existing_data:
                return JsonResponse({
                    'message': 'Data already exists',
                    'data': {
                        'buyer_name' :existing_plan.buyer_name,
                        'buyer':existing_plan.buyer,
                        'styleno' : existing_plan.styleno,
                        'quantity' : existing_plan.quantity,
                        'planing' :existing_plan.id,
                        'color' :existing_plan.color,
                        'mt_id' : existing_data.id,
                        'ourref':existing_plan.ourref,
                        'unit_id':existing_plan.unit.id,
                        'floor_id':existing_plan.floor.id,
                        'line_id':existing_plan.line.id,
                        'delvdate':existing_plan.delvdate,
                    }
                }, status=200)
            else:
                new_data = SwingLineInputMt.objects.create(
                    planing =existing_plan,
                )
                return JsonResponse({
                    'message': 'Data saved successfully',
                    'data': {
                        'buyer_name' :existing_plan.buyer_name,
                        'buyer':existing_plan.buyer,
                        'styleno' : existing_plan.styleno,
                        'quantity' : existing_plan.quantity,
                        'color' :existing_plan.color,
                        'planing' :existing_plan.id,
                        'mt_id': new_data.id ,
                        'ourref':existing_plan.ourref,
                        'unit_id':existing_plan.unit.id,
                        'floor_id':existing_plan.floor.id,
                        'line_id':existing_plan.line.id,
                        'delvdate':existing_plan.delvdate, 
                    }
                }, status=200)
            
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

    def post(self, request):
        try:
            data = json.loads(request.body)
            size = data.get('size', '')
            quantity = data.get('quantity', 0)
            id = data.get('mt_id')
            # print("Swing Dt Data", data)

            swing_mt_data = SwingLineInputMt.objects.filter(id=id).first()
            if swing_mt_data:
                dt_existing_data = SwingLineInputDt.objects.filter(mt_id=swing_mt_data, size=size).first()
                if dt_existing_data:
                    prv_quantity =dt_existing_data.quantity
                    dt_existing_data.quantity = quantity + prv_quantity
                    dt_existing_data.save()
                    return JsonResponse({'message': 'Size Data already exists'}, status=200)
                else:
                    new_dt_data = SwingLineInputDt(mt_id=swing_mt_data, size=size, quantity=quantity)
                    new_dt_data.save()
                    return JsonResponse({'message': 'Data saved successfully'}, status=201)
            else:
                return JsonResponse({'message': 'Sewing line input mt with id {} does not exist'.format(id)}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get_id_by_size_data(self,request):
        mt_id = request.GET.get('mt_id')
        print("mt_id",mt_id)
        
        try:
            plan_data = SewingPlanning.objects.get(id=mt_id)
            exists = SwingLineInputMt.objects.get(planing__id=plan_data.id)
        except SewingPlanning.DoesNotExist:
            exists = SwingLineInputMt.objects.get(id=mt_id)
        
        exists = SwingLineInputMt.objects.get(planing__id=plan_data.id)
        size_dt_data = SwingLineInputDt.objects.filter(mt_id=exists)
        
        size_dt_list = []
        for obj in size_dt_data:
            size_dt_list.append({
                'id': obj.id,
                'size': obj.size,
                'quantity':obj.quantity
                
            })
        
        return size_dt_list
    
    @csrf_exempt
    def get(self, request):
        size_dt_list = self.get_id_by_size_data(request)
        return JsonResponse(size_dt_list, safe=False)
    
    
    
class SewingLineInputMtView(View):
    def get_mt_by_line(self, request):
        line_id = request.GET.get('line_id')
        mt_data = SwingLineInputMt.objects.filter(line_id=line_id).order_by('-id')
        return mt_data
        
    @csrf_exempt
    def get(self, request):
        mt_data = self.get_mt_by_line(request)
        mt_list = list(mt_data.values())
        context ={
            'mt_list':mt_list,
        }
        return JsonResponse(context, safe=False)
    