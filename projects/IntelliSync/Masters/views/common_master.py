from django.views import View
from django.shortcuts import redirect, render
from IntelliSync_db.models import CommonMaster, CommonMasterType, name_code_list
from IS_Nexus.functions import messages
from django.shortcuts import get_object_or_404
from IntelliSync_db.models.common_master import non_editable_list, first_level_list, second_level_list
from django.db import connections


class CommonMasterView(View):
    def get(self, request):

        # for data in non_editable_list:
        CommonMasterType.objects.filter(code__in=non_editable_list).update(editable=False)
        CommonMasterType.objects.filter(code__in=first_level_list).update(label_type=1)
        CommonMasterType.objects.filter(code__in=second_level_list).update(label_type=2)

        # cursor = connections['main_db'].cursor()
        # sql = 'select name, value, remark, type_id from common_master order by type_id'
        # cursor.execute(sql)
        # data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        # for item in data:
        #     name = item['name']
        #     value = item['value']
        #     remark = item['remark']
        #     master_type = item['type_id'] 

        #     master_type = CommonMasterType.objects.get(id=master_type)

        #     CommonMaster.objects.create(
        #         master_type = master_type,
        #         name = name,
        #         value = value,
        #         remark = remark,
        #     )

        master_types_list = CommonMasterType.objects.filter(is_active=True, label_type='0')
        master_list = CommonMaster.objects.all().values(
            'id', 'master_type__name','name', 'value', 
            'remark', 'master_type__editable', 'created_at', 
            'is_active'
        ).order_by('master_type__name')

        action = request.GET.get('action')
        pk = request.GET.get("pk")

        context = {
            'master_list' : master_list,
            'master_types_list' : master_types_list
        }

        # Delete Record
        if pk and action == 'delete':
            try:
                if data := get_object_or_404(CommonMaster, id=pk):
                    data.delete()
                    messages.delete(request)
                else:
                    return redirect('main_master_page')
                
            except Exception as e:
                print("\n", e, "\n")
                messages.delete_error(request)
        
        # Fetch data to Update Records
        elif pk and action == 'update':
            data = get_object_or_404(CommonMaster, id=pk)
            context['data'] = data

            if not data:
                return redirect('main_master_page')
        
        return render(request, 'common_master.html', context)


    def post(self, request):
        master_type = request.POST.get("master_type")
        name = request.POST.get("name")
        value = request.POST.get("value")
        remark = request.POST.get("remark")
        is_active = bool(request.POST.get("is_active"))
        action = request.GET.get('action')
        pk = request.GET.get('pk')

        # Check foreign key key data 
        try:
            master_type = CommonMasterType.objects.get(id=master_type) 

        except Exception as e:
            messages.unexpected_error(request)

        if master_type and name:
            # Update Record
            if pk and action == 'update':
                
                try:
                    data = get_object_or_404(CommonMaster, id=pk)
                    data.master_type = master_type
                    data.name = name
                    data.value = value
                    data.remark = remark
                    data.is_active = is_active
                    data.save()
                    messages.update(request)
                except Exception as e:
                    print('\n', e, '\n')
                    messages.update_error(request)

            # Create
            elif not pk:
                try:
                    CommonMaster.objects.create(
                        master_type = master_type,
                        name = name,
                        value = value,
                        remark = remark,
                        is_active = is_active
                    )
                    messages.saved(request)
                except Exception as e:
                    messages.saved_error(request)
                    print('\n', e, '\n')
        
        else:
            messages.form_error(request)
        return redirect('common_master_page')

