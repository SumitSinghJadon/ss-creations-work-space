from django.views import View
from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest, JsonResponse
import pandas as pd
from ERP_db.models import Party, Style
from QMS_db.models import ObDetail, ObMaster
from IS_Nexus.functions import queryset_to_json
from IS_Nexus.functions.shortcuts import formate_date


class UploadOB(View):
    def get(self, request):
        flag = request.GET.get("flag")
        buyer_list = Party.objects.using('erp_db').all()[:5]

        if flag == "get_style_buyer":
            buyer = request.GET.get("id")
            style_list = Style.objects.filter(buyer=buyer).values('styleno')
            data = queryset_to_json(style_list)
            return JsonResponse(data, safe=False)
        
        context = {
            "buyer_list" : buyer_list
        }
        return render(request, 'upload_ob.html', context) 


    def post(self, request):
        if 'file' not in request.FILES:
            return HttpResponseBadRequest("File not provided")
        file = request.FILES['file']

        try:
            df = pd.read_excel(file)
            
            if df.empty:
                return Http404("No data found in the file")
            
            df = df.fillna('')
            columns = df.columns.tolist()
            data = df.to_dict(orient='records')

        except Exception as e:
            return HttpResponseBadRequest(f"Error reading the file: {str(e)}")
        

        mt_data = ObMaster.objects.create(
            buyer_code  = request.POST.get("buyer"),
            buyer_name  = request.POST.get("buyer_name"),
            style       = request.POST.get("style_code"),
            line_sum    = request.POST.get("line_sum"),
            ob_no       = request.POST.get("ob_no"),
            ob_date     = formate_date(request.POST.get("ob_date")),
            line_sam    = request.POST.get("line_sam"),
            re_cutting  = request.POST.get("re_cutting"),
            kaz_button  = request.POST.get("kaz_button"),
            other       = request.POST.get("other")
        )

        total_sam = 0
        dt_data_list = []

        for row in data:
            total_sam = total_sam + float(row['SAM'])
            dt_data = ObDetail.objects(
                parts  = row["Parts"],
                operation  = row["Operation"],
                type_of_machine  = row["Type Of Machine"],
                attachments  = row["Attachments"],
                sam  = row["SAM"],
                theoretical_manpower  = row["Theoretical Manpower"],
                planned_work_station  = row["Planned Work Station"],
                target_100_pcs  = row["Target @ 100% PCS/Hr"],
                target_60_pcs  = row["Target @ 60% PCS/Hr"],
                seam_length  = row["SEAM LENGTH"],
                remark  = row["Remark"]
            )
            dt_data_list.append(dt_data)

        ObDetail.objects.bulk_create(dt_data_list)

        mt_data.total_same = total_sam
        mt_data.save()

        if data:
            buyer_list = Party.objects.using('erp_db').all()[:5]
            context = {
                'columns' : columns,
                'data': data,
                'buyer_list' : buyer_list
            }
            return render(request, 'upload_ob.html', context)
        else:
            return Http404("No data found in the file")
