from django.shortcuts import render, redirect
from django.views import View
from QMS_db.models import OrderDt
from QMS_db.models import OrderMt  
from django.db import connections
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
from django.http import JsonResponse




class OrderDtView(View):
    
    @method_decorator(csrf_exempt)  # Apply CSRF exemption to the entire class
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    @csrf_exempt
    def get(self, request):
        ourref = request.GET.get('ourref')
        style_no = request.GET.get('style_no')
        buyer_code = request.GET.get('buyer')
        color = request.GET.get('color')
        print (ourref,"2",style_no,"3",buyer_code,"4",color)
        
        # SQL query to fetch data
        # sql = f'''EXEC GET_BUYER_COLOR_SIZE_QTY 'B000000029','GMA/000007','HAEDI BLOUSE','PINK YELLOW LIGHT'
        # '''
        sql = f''' EXEC GET_BUYER_COLOR_SIZE_QTY '{ourref}' '''

        print(sql)
        cursor = connections['erp_db'].cursor()
        cursor.execute(sql)
        data = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        #return data
        data = cursor.fetchall()
        print("data aaya",data)
        context = {
            'data': data,
            'ourref': ourref,
            'style_no': style_no,
            
        }
        # return render(request, 'order_dt_view.html', context)
        return JsonResponse (context)
    
    def post(self, request):
            size = request.POST.get('size')
            quantity = request.POST.get('quantity')
            order_mt_id = request.POST.get('order_mt_id')
            try:
                order_mt = OrderMt.objects.get(pk=order_mt_id)
            except OrderMt.DoesNotExist:
                return JsonResponse("Order Dose Not Exist")

            if OrderDt.objects.filter(order_mt=order_mt).exists():
                return JsonResponse("Order Exist") 

            order_dt = OrderDt.objects.create(order_mt=order_mt, size=size, quantity=quantity)
            return redirect("OrderDtView2")





class OrderDtView2(View):
    
    @method_decorator(csrf_exempt)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        order_dts = OrderDt.objects.all().values()
        order_mts = OrderMt.objects.all().values()
        context ={
            'order_dts' : list(order_dts),
            'order_mts' : list(order_mts)
        }
        return JsonResponse(context,safe=False)
    
    # def post(self,request):
        
    

