from django.views import View
from django.shortcuts import redirect, render
from IntelliSync_db.models import CommonMaster, CommonMasterType, FirstLevelMaster, SecondLevelMaster
from django.http import JsonResponse
from IS_Nexus.functions import queryset_to_json
from IS_Nexus.functions import messages


class FirstLevelMasterView(View):
    def get(self, request):
        # Form Data
        common_master_type_list = CommonMasterType.objects.filter(is_active=True, label_type='0').values('id', 'name')
        master_type_list = CommonMasterType.objects.filter(is_active=True, label_type='1').values('id', 'name')
        
        action = request.GET.get('action')
        pk = request.GET.get("pk")

        # Table data
        master_list = FirstLevelMaster.objects.all().values(
            'id', 'common_master_type__name', 'common_master_type__code', 'common_master__name', 'master_type__name', 'name', 'value', 'code', 'remark', 'is_active'
        ).order_by('common_master_type__name')
        context = {
            # Form
            'master_type_list':master_type_list,
            'common_master_type_list':common_master_type_list,
            # Table
            'master_list':master_list,
        }

        # Ajax response
        if action == 'get_common_master_list':
            type_id = request.GET.get("type_id")
            parent_list = CommonMaster.objects.filter(master_type=type_id).values('id','name')
            parent_list = queryset_to_json(parent_list)
            return JsonResponse(parent_list ,safe=False)

        elif pk and action == 'delete':
            try:
                if data := FirstLevelMaster.objects.filter(id=pk):
                    data.delete()
                    messages.delete(request)
                else:
                    return redirect('first_level_master_page')
                
            except Exception as e:
                print("\n", e, "\n")
                messages.delete_error(request)
        
        # Fetch data to Update Records
        elif pk and action == 'update':
            if data:= FirstLevelMaster.objects.get(id=pk):
                common_master_list = CommonMaster.objects.filter(master_type=data.common_master_type).values('id','name')
                context['data'] = data
                context['common_master_list'] = common_master_list
            else:
                return redirect('first_level_master_page')

        return render(request, 'first_level_master.html', context)


    def post(self, request):
        common_master_type = request.POST.get('common_master_type')
        common_master = request.POST.get('common_master')
        master_type = request.POST.get('master_type') # First level master type
        name = request.POST.get("name")
        value = request.POST.get("value")
        remark = request.POST.get("remark")
        is_active = request.POST.get("is_active", False)
        pk = request.GET.get("pk") # If user want to update the records
        action = request.GET.get("action") 

        if common_master_type and common_master and master_type:
            try:
                common_master_type = CommonMasterType.objects.get(id=common_master_type)
                common_master = CommonMaster.objects.get(id=common_master)
                master_type = CommonMasterType.objects.get(id=master_type)

                if action == 'update' and pk:
                    if instance := FirstLevelMaster.objects.filter(id=pk):
                        instance.update(
                            common_master_type = common_master_type,
                            common_master = common_master,
                            master_type = master_type,
                            name = name,
                            value = value,
                            remark = remark,
                            is_active = is_active,
                        )
                        messages.update(request)
                    else:
                        messages.update_error(request)
                    
                elif not pk:
                    FirstLevelMaster.objects.create(
                        common_master_type = common_master_type,
                        common_master = common_master,
                        master_type = master_type,
                        name = name,
                        value = value,
                        remark = remark,
                        is_active = is_active,
                    )
            except Exception as e:
                print('\n', e, '\n')
                messages.unexpected_error(request)
        else:
            messages.form_error(request) 
        return redirect('first_level_master_page')

