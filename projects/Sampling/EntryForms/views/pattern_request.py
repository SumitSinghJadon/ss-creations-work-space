from django.shortcuts import render, redirect
from django.views import View
from Sampling_db.models import PatternRequestMt
from django.contrib import messages
from datetime import datetime , timedelta

class PatternRequestView(View):
    def get(self, request):
        number_list = PatternRequestMt.objects.all().using('default')
        context ={
            'number_list':number_list
        }
        # print("\n\n", data, "\n\n")
        return render(request, 'pattern_request.html',context)
    

    def post(self, request):
        next_no = PatternRequestMt.objects.all().last()
        if not next_no:
            next_no = 1
        else:
            next_no = int(next_no.id) + 1
        curr_date = datetime.today().strftime('%d%m%y') 
        request_no      = f'ptrn/{curr_date}/{next_no}'
        # request_no = request.POST.get('request_no')
        request_date = request.POST.get("request_date")
        request_type = request.POST.get("request_type")
        pattern_stage = request.POST.get("pattern_stage")
        pattern_type = request.POST.get("pattern_type")
        merchant = request.POST.get("merchant")
        buyer_name = request.POST.get("buyer_name")
        style_name = request.POST.get("style_name")
        color_name = request.POST.get("color_name")
        pattern_master = request.POST.get("pattern_master")
        expected_del_date = request.POST.get("expected_del_date")
        expected_del_time = request.POST.get("expected_del_time")
        

        PatternRequestMt.objects.create(
            request_no = request_no,
            request_date = request_date,
            request_type = request_type,
            pattern_stage = pattern_stage,
            pattern_type = pattern_type,
            merchant = merchant,
            buyer_name = buyer_name,
            style_name = style_name,
            color_name = color_name,
            pattern_master = pattern_master,
            expected_del_date = expected_del_date,
            expected_del_time = expected_del_time,
        )
        messages.success(request, "Success! The entry has been created.")
        return redirect ('pattern_request_page')