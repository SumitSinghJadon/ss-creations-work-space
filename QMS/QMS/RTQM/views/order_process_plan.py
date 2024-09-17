from django.views import View
from django.http import JsonResponse
from QMS_db.models import OrderMt

class OrderProcessPlan(View):
    template_name = 'order_process_plan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_mts'] = OrderMt.objects.all()
        print(context) 
        return context
      
    def post(self, request, *args, **kwargs):
        buyer = request.POST.get('buyer')
        data = {}
        if buyer:
            order_mt = OrderMt.objects.filter(buyer=buyer).first()
            if order_mt:
                data['buyer_order_no'] = order_mt.buyer_order_no
                data['ref_no'] = order_mt.ourref_no
                data['quantity'] = order_mt.quantity
                data['color'] = order_mt.color
                data['style_no'] = order_mt.style_no
        return JsonResponse(data)
    
    def get(self, request):
        pass 
        

