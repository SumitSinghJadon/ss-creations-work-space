from django.shortcuts import render, redirect
from django.views import View
from django.db import connections
from django.http import JsonResponse
from QMS_db.models import OrderMt, OrderDt
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
from IS_Nexus.functions.data_conversion import queryset_to_json
from django.core import serializers
import json
from datetime import datetime

class SendToQMS(View):
    def get(self, request):
        def get_buyer_list():
                       
            cursor = connections['erp_db'].cursor()
            sql = '''
                SELECT distinct t2.buyer, t3.party_name from ExpoHead t2
                join party t3 on t3.party_code = t2.buyer
                where t2.buyer is not NULL and t3.isbuyer = 1 and t2.closed in ('U', 'P')
                order by t3.party_name;
            '''
           
            cursor.execute(sql)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()
            return data_list or None
        
        def get_order_data(filter=''):
            cursor = connections['erp_db'].cursor() 
            sql = f'''
                SELECT TOP 50 t3.delvdate, t1.ourref, t1.styleno, t1.color, t1.totalqty, 
                t2.buyer, t2.season, t2.totalpcs, t2.buyord, t2.sizetype, t4.party_name from ExpoLotDet t1 
                join ExpoHead t2 on t1.ourref = t2.ourref join ExpoLot t3 on t1.ourref = t3.ourref join party t4 
                on t4.party_code = t2.buyer
                {filter}
            '''
            
            
            cursor.execute(sql)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return data_list or None 
            
        

        context = {
            'data' : get_order_data(),
            'buyer_list' : get_buyer_list()
        }
        # return render(request,'send_to_qms.html', context) 
        return JsonResponse (context) 
    

    def post(self, request):
        pass 




# @csrf_exempt
class SendToQMS2(View):
    
    @method_decorator(csrf_exempt)  # Apply CSRF exemption to the entire class
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    """ Fetch data from ERP and save in IS_QMS_db """
    def prepare_sql(self, request):
        """ Create query to fetch data from ERP with Filter (Selected by user)  """
        filter_string = 'WHERE t1.ourref is not NULL'
        buyer_filter = request.GET.get('buyer_filter')
        ref_filter = request.GET.get('ref_filter')
        style_filter = request.GET.get('style_filter')
        # print(buyer_filter,ref_filter,style_filter)
        

        if buyer_filter: filter_string += f" and t2.buyer = '{buyer_filter}'"
        if ref_filter: filter_string += f" and t1.ourref = '{ref_filter}'"    
        if style_filter: filter_string += f" and t1.styleno = '{style_filter}'"

        if buyer_filter or ref_filter or style_filter: 
            cursor = connections['erp_db'].cursor()
                
            sql = f'''
                SELECT DISTINCT t3.delvdate, t1.ourref, t1.styleno, t1.color, t1.totalqty, 
                t2.buyer, t2.season, t2.totalpcs, t2.buyord, t2.sizetype, t4.party_name
                from ExpoLotDet t1
                join ExpoHead t2 on t1.ourref = t2.ourref 
                join ExpoLot t3 on t1.ourref = t3.ourref
                join party t4 on t4.party_code = t2.buyer { filter_string }
            '''
           
            
            cursor.execute(sql)
            # print(sql)
            
            
            data = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            # print(data)
            return data
        else:
            response_data ={} # Add By Sudhir
            response_data['csrf_token'] = get_token(request)  # Add By Sudhir
            return JsonResponse (response_data) # Add By Sudhir


    @csrf_exempt
    def get(self, request):
        """ Handle Get Request """
        cursor = connections['erp_db'].cursor()
        
        # Handle Ajax Request 
        flag = request.GET.get("flag")
        buyer = request.GET.get('buyer')
        style = request.GET.get('style')

        if flag == 'get_style_by_buyer' and buyer:
            sql = f'''
                SELECT distinct t1.styleno from ExpoLotDet t1
                join ExpoHead t2 on t1.ourref = t2.ourref
                where t2.buyer = '{buyer}' and 
                t1.styleno != '' and t2.closed in ('U', 'P')
            '''
            cursor.execute(sql)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return JsonResponse(data_list, safe=False)


        elif flag == 'get_ref_by_buyer_&_style' and style and buyer:
            sql = '''SELECT distinct t2.ourref from ExpoLotDet t1
                    join ExpoHead t2 on t1.ourref = t2.ourref
                    where t2.buyer = 'B000000002' and 
                    t1.styleno = 'DW VIENNA' and t2.closed in ('U', 'P')
            '''
            cursor.execute(sql)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return JsonResponse(data_list, safe=False)
        
        # Send Default Data
        sql = '''
            SELECT distinct t2.buyer, t3.party_name from ExpoHead t2
            join party t3 on t3.party_code = t2.buyer
            where t2.buyer is not NULL and t3.isbuyer = 1 and t2.closed in ('U', 'P')
            order by t3.party_name;
        '''
        cursor.execute(sql)
        buyer_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        # Get all data
        data = self.prepare_sql(request)
        csrf_token = get_token(request)  # Add By Sudhir
        # convert_data = queryset_to_json(data)
        
        context = {
            'data' : data,
            'buyer_list' : buyer_list,
            'csrf_token' : csrf_token,  # Add By Sudhir
            
            
        }
        # return render(request,'send_to_qms.html', context)
       
        return JsonResponse(context) # Add By Sudhir
        

   

    @csrf_exempt
    def post(self, request):
        """ Fetch selected data from user and save it in OrderMt and save in (OrderDt based on OrderMT Id) """
        # data_list = self.prepare_sql(request)
        request_data = json.loads(request.body.decode('utf-8'))  
        # print("Data received from frontend:", request_data)
        # selected_ref_no = request.POST.getlist('request_data')
        cursor = connections['erp_db'].cursor()

        # data_list = json.loads(data_list)
        # print("backend_data" , data_list)

        for item in request_data:
            if item:
                try:
                    delvdate = datetime.strptime(item['delvdate'], "%Y-%m-%dT%H:%M:%S").date()
                    saved_data = OrderMt.objects.create(
                        buyer=item['party_name'],
                        buyer_order_no=item['buyord'],
                        ourref_no=item['ourref'],
                        style_no=item['styleno'],
                        delivery_date=delvdate,
                        quantity=item['totalpcs'],
                        color=item['color'],
                        style_name=item['styleno'],
                        Style_category="NA"
                    )

                    sql = f"""EXEC GET_BUYER_COLOR_SIZE_QTY 'B000000197','GMA/003411','FADO NIGHTDRESS','Blue Milange'"""
                    cursor = connections['is_app_db'].cursor()
                    cursor.execute(sql)
                    data=[{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

                    for item in data:
                        try:
                            sa = OrderDt.objects.create(order_mt = saved_data, size=item['sizeval'], quantity = item['qty'])
                            sa.save()
                        
                        except Exception as e:
                            print("error ->", e)

                except Exception as e:
                    print("error ->", e)

        return JsonResponse({'error': 'Invalid request method'})












# # @csrf_exempt
# class SendToQMS2(View):
#     """ Fetch data from ERP and save in IS_QMS_db """
#     @csrf_exempt
#     def prepare_sql(self, request):
#         """ Create query to fetch data from ERP with Filter (Selected by user)  """
#         filter_string = 'WHERE t1.ourref is not NULL'

#         buyer_filter = request.GET.get('buyer_filter')
#         ref_filter = request.GET.get('ref_filter')
#         style_filter = request.GET.get('style_filter')

#         if buyer_filter: filter_string += f" and t2.buyer = '{buyer_filter}'"
#         if ref_filter: filter_string += f" and t1.ourref = '{ref_filter}'"    
#         if style_filter: filter_string += f" and t1.styleno = '{style_filter}'"

#         if buyer_filter or ref_filter or style_filter: 
#             cursor = connections['erp_db'].cursor()
                
#             sql = f'''
#                 SELECT TOP 300 t3.delvdate, t1.ourref, t1.styleno, t1.color, t1.totalqty, 
#                 t2.buyer, t2.season, t2.totalpcs, t2.buyord, t2.sizetype, t4.party_name
#                 from ExpoLotDet t1
#                 join ExpoHead t2 on t1.ourref = t2.ourref 
#                 join ExpoLot t3 on t1.ourref = t3.ourref
#                 join party t4 on t4.party_code = t2.buyer { filter_string }
#             '''
            
#             cursor.execute(sql)
            
#             data = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
#             return data
#         else:
#             response_data ={} # Add By Sudhir
#             response_data['csrf_token'] = get_token(request)  # Add By Sudhir
#             return JsonResponse (response_data) # Add By Sudhir

#     @csrf_exempt
#     def get(self, request):
#         """ Handle Get Request """
#         cursor = connections['erp_db'].cursor()
        
#         # Handle Ajax Request 
#         flag = request.GET.get("flag")
#         buyer = request.GET.get('buyer')
#         style = request.GET.get('style')

#         if flag == 'get_style_by_buyer' and buyer:
#             sql = f'''
#                 SELECT distinct t1.styleno from ExpoLotDet t1
#                 join ExpoHead t2 on t1.ourref = t2.ourref
#                 where t2.buyer = '{buyer}' and 
#                 t1.styleno != '' and t2.closed in ('U', 'P')
#             '''
#             cursor.execute(sql)
#             data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
#             return JsonResponse(data_list, safe=False)


#         elif flag == 'get_ref_by_buyer_&_style' and style and buyer:
#             sql = '''SELECT distinct t2.ourref from ExpoLotDet t1
#                     join ExpoHead t2 on t1.ourref = t2.ourref
#                     where t2.buyer = 'B000000002' and 
#                     t1.styleno = 'DW VIENNA' and t2.closed in ('U', 'P')
#             '''
#             cursor.execute(sql)
#             data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
#             return JsonResponse(data_list, safe=False)
        
#         # Send Default Data
#         sql = '''
#             SELECT distinct t2.buyer, t3.party_name from ExpoHead t2
#             join party t3 on t3.party_code = t2.buyer
#             where t2.buyer is not NULL and t3.isbuyer = 1 and t2.closed in ('U', 'P')
#             order by t3.party_name;
#         '''
#         cursor.execute(sql)
#         buyer_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

#         # Get all data
#         data = self.prepare_sql(request)
#         csrf_token = get_token(request)  # Add By Sudhir
        
#         context = {
#             'data' : data,
#             'buyer_list' : buyer_list,
#             'csrf_token' : csrf_token,  # Add By Sudhir
            
            
#         }
#         # return render(request,'send_to_qms.html', context)
       
#         return JsonResponse (context) # Add By Sudhir
        

#     @csrf_exempt
#     def post(self, request):
#         """ Fetch selected data from user and save it in OrderMt and save in (OrderDt based on OrderMT Id) """
#         data_list = self.prepare_sql(request)
#         selected_ref_no = request.POST.getlist('items')
#         cursor = connections['erp_db'].cursor()

#         for item in selected_ref_no:
#             item = next((d for d in data_list if d['ourref'] == item), None)

#             if item:
#                 try:
#                     saved_data = OrderMt.objects.create(
#                         buyer=item['party_name'],
#                         buyer_order_no=item['buyord'],
#                         ourref_no=item['ourref'],
#                         style_no=item['styleno'],
#                         delivery_date=item['delvdate'],
#                         quantity=item['totalpcs'],
#                         color=item['color'],
#                         style_name="NA",
#                         Style_category="NA"
#                     )

#                     sql = f"""EXEC GET_BUYER_COLOR_SIZE_QTY 'B000000197','GMA/003411','FADO NIGHTDRESS','Blue Milange'"""
#                     cursor = connections['is_app_db'].cursor()
#                     cursor.execute(sql)
#                     data=[{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
 
#                     for item in data:
#                         try:
#                             print(item)
#                             sa = OrderDt.objects.create(order_mt = saved_data, size=item['sizeval'], quantity = item['qty'])
#                             sa.save()

#                         except Exception as e:
#                             print("error ->", e)

#                 except Exception as e:
#                     print("error ->", e)

#         return redirect("Send_To_QMS")



 # @csrf_exempt
    # def post(self, request):
    #     """ Fetch selected data from user and save it in OrderMt and save in (OrderDt based on OrderMT Id) """
    #     data_list = self.prepare_sql(request)
    #     data_list_c = json.loads(data_list)
    #     request_data = json.loads(request.body.decode('utf-8'))  # Decode JSON data
    #     print("Data received from frontend:", request_data)
    #     selected_ref_no = request.POST.getlist('request_data')
    #     cursor = connections['erp_db'].cursor()
    #     # print(request_data)
    #     for item in request_data:
    #         print("Selected item:", item)
    #         item = next((d for d in data_list_c if d['ourref'] == item), None)
    #         print("Matched item:", item)
            
    #         # item = next((d for d in data_list if d['ourref'] == item), None)

    #         if item:
    #             try:
    #                 saved_data = OrderMt.objects.create(
    #                     buyer=item['party_name'],
    #                     buyer_order_no=item['buyord'],
    #                     ourref_no=item['ourref'],
    #                     style_no=item['styleno'],
    #                     delivery_date=item['delvdate'],
    #                     quantity=item['totalpcs'],
    #                     color=item['color'],
    #                     style_name="NA",
    #                     Style_category="NA"
    #                 )
    #                 print("saved data",saved_data)

    #                 sql = f"""EXEC GET_BUYER_COLOR_SIZE_QTY 'B000000197','GMA/003411','FADO NIGHTDRESS','Blue Milange'"""
    #                 cursor = connections['is_app_db'].cursor()
    #                 cursor.execute(sql)
    #                 data=[{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
 
    #                 for item in data:
    #                     try:
    #                         print(item)
    #                         sa = OrderDt.objects.create(order_mt = saved_data, size=item['sizeval'], quantity = item['qty'])
    #                         sa.save()
                           
    #                     except Exception as e:
    #                         print("error ->", e)

    #             except Exception as e:
    #                 print("error ->", e)

    #     # return redirect("Send_To_QMS")
    #     return JsonResponse({'error': 'Invalid request method'})
