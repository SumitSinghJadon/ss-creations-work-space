from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from App_db.models import TnaTemplateMt, TnaTemplateDt
from IS_Nexus.functions.shortcuts import execute_sql, get_next_number
from IS_Nexus.functions.data_conversion import queryset_to_json
from IntelliSync_db.models import CommonMaster, FirstLevelMaster


class TnaTemplateView(View):
    def get(self, request):
        flag = request.GET.get("flag")
        tid = request.GET.get("tid")

        if flag == 'get_activity_by_group':
            ag_id = request.GET.get("ag_id")
            activity_list  = FirstLevelMaster.objects.filter(master_type__code='CT-27', is_active=True, common_master=ag_id).values('id', 'name')
            return JsonResponse(queryset_to_json(activity_list), safe=False)

        elif flag == 'get_type_by_activity':
            at_id = request.GET.get("at_id")
            data  = FirstLevelMaster.objects.get(id=at_id)
            return HttpResponse(data.value)
        
        elif flag == 'get_activity_by_name':
            an_id = request.GET.get("an_id")
            data = TnaTemplateMt.objects.filter(id=an_id)
            return HttpResponse(data)

        else:
            # Add New
            sql = "SELECT distinct t2.party_code, t2.party_name from ExpoHead t1 join party t2 on t1.buyer = t2.party_code"
            buyer = execute_sql('erp_db', sql)
            activity_group_list = CommonMaster.objects.filter(master_type__code ='CT-26', is_active=True)
            base_activity_list  = FirstLevelMaster.objects.filter(master_type__code='CT-27', is_active=True).values('id', 'name')
            
            context = {
                "buyer" : buyer,
                "activity_group_list" : activity_group_list,
                "base_activity_list"  : base_activity_list,
                "dt_data"             : '1'
            }

            # Update 
            if tid:
                data = TnaTemplateMt.objects.get(id=tid)
                dt_data = TnaTemplateDt.objects.filter(tna_mt=tid).order_by('seq_no')
                context['data'] = data
                context['dt_data'] = dt_data

            return render(request, 'T&A_Template.html', context)


    def post(self, request):
        tid           = request.POST.get("tid")
        buyer_code    = request.POST.get('buyer')
        days_from     = request.POST.get('days_from')
        days_to       = request.POST.get('days_to')
        template_desc = request.POST.get('template_desc')
        template_name = request.POST.get('template_name')

        sql = f"SELECT party_name from party where party_code = '{buyer_code}'"
        buyer = execute_sql('erp_db', sql)
        buyer_name = buyer[0]['party_name']

        # MT Update Data
        if tid:
            mt_data = TnaTemplateMt.objects.filter(id=tid).update(
                template_name = template_name,
                template_desc = template_desc,
                buyer_code    = buyer_code,
                buyer_name    = buyer_name,
                days_from     = days_from,
                days_to       = days_to,
            )
            mt_data = TnaTemplateMt.objects.get(id=tid)
            TnaTemplateDt.objects.filter(tna_mt=mt_data).delete()
        
        # MT Create Case
        else:
            template_no    = get_next_number(TnaTemplateMt, 'TNA')
            mt_data = TnaTemplateMt.objects.create(
                template_no   = template_no,
                template_name = template_name,
                template_desc = template_desc,
                buyer_code    = buyer_code,
                buyer_name    = buyer_name,
                days_from     = days_from,
                days_to       = days_to,
            )
        

        seq_no_list              = request.POST.getlist('seq_no')
        activity_group_list      = request.POST.getlist('activity_group')
        activity_name_list       = request.POST.getlist('activity_name')
        activity_type_list       = request.POST.getlist('activity_type')
        days_action_list         = request.POST.getlist('days_action')
        days_req_list            = request.POST.getlist('days_req')
        days_after_before_list   = request.POST.getlist('days_after_before')
        running_days_list        = request.POST.getlist('running_days')
        base_activity_list       = request.POST.getlist('base_activity')
        status_list              = request.POST.getlist('status')

        for seq_no, activity_group, activity_name, activity_type, days_req, days_after_before, running_days, base_activity, status, days_action in zip(seq_no_list, activity_group_list, activity_name_list, activity_type_list, days_req_list,days_after_before_list, running_days_list, base_activity_list, status_list, days_action_list):
            activity_group = CommonMaster.objects.get(id=int(activity_group))
            activity_name  = FirstLevelMaster.objects.get(id=int(activity_name))
            base_activity  = FirstLevelMaster.objects.get(id=int(base_activity))
            
            TnaTemplateDt.objects.create(
                tna_mt            = mt_data,
                seq_no            = seq_no,
                activity_group    = activity_group,
                activity_name     = activity_name,
                activity_type     = activity_type,
                days_action       = days_action,
                days_req          = days_req or 0,
                days_after_before = days_after_before or 0,
                running_days      = running_days or 0,
                base_activity     = base_activity,
                status            = eval(status)
            )

        messages.success(request, "Success! The entry has been created.")
        return redirect ('T&A_Template_History_page')
