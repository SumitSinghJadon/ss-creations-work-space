# from django.views import View
# from django.shortcuts import render
# from IntelliSync_db.models import LocationMaster
# from django.db import connections
# from datetime import datetime
# import json

# class OnTimeDeliveryView(View):
#     def get(self, request):
#         if request.GET.get('from_date'):
#             from_date = request.GET.get('from_date')
#             from_date_filt = datetime.strptime(from_date, '%d-%m-%Y').strftime('%Y-%m-%d')
#         else:
#             from_date = datetime.now().strftime("01-%m-%Y")
#             from_date_filt = datetime.now().strftime("%Y-%m-01")

#         if request.GET.get('to_date'):
#             to_date = request.GET.get('to_date')
#             to_date_filt = datetime.strptime(to_date, '%d-%m-%Y').strftime('%Y-%m-%d')
#         else:
#             to_date = datetime.now().strftime("%d-%m-%Y")
#             to_date_filt = datetime.now().strftime("%Y-%m-%d")

#         unit_list = LocationMaster.objects.filter(is_active=True)
#         data_list = []
#         unit_code = ''
#         unit_code_erp = None

#         if request.GET.get('unit_code'):
#             unit_code = request.GET.get('unit_code')
#             unit_code_erp = LocationMaster.objects.get(payroll_code=unit_code).erp_code

#         sql_query = f"""EXEC [GET_SALE_TURNOVER] '{from_date_filt}', '{to_date_filt}', {f"'{unit_code_erp}'" if unit_code_erp else 'NULL'}, 'otdunitsummary'"""

#         with connections['default'].cursor() as cursor:
#             cursor.execute(sql_query)
#             data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

#         json_result = json.dumps(data_list)

#         context = {
#             'unit_code_erp': unit_code_erp,
#             'unit_list': unit_list,
#             'unit_code': unit_code,
#             'from_date': from_date,
#             'to_date': to_date,
#             'from_date_filt': from_date_filt,
#             'to_date_filt': to_date_filt,
#             'data_list': data_list,
#         }
#         return render(request, 'on_time_delivery.html', context)

from django.views import View
from django.shortcuts import render
from IntelliSync_db.models import LocationMaster
from django.db import connections
from datetime import datetime
import json

class OnTimeDeliveryView(View):
    def get(self, request):
        if request.GET.get('from_date'):
            from_date = request.GET.get('from_date')
            from_date_filt = datetime.strptime(from_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            from_date = datetime.now().strftime("01-%m-%Y")
            from_date_filt = datetime.now().strftime("%Y-%m-01")

        if request.GET.get('to_date'):
            to_date = request.GET.get('to_date')
            to_date_filt = datetime.strptime(to_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            to_date = datetime.now().strftime("%d-%m-%Y")
            to_date_filt = datetime.now().strftime("%Y-%m-%d")

        unit_list = LocationMaster.objects.filter(is_active=True)
        data_list = []
        unit_code = ''
        unit_code_erp = None

        if request.GET.get('unit_code'):
            unit_code = request.GET.get('unit_code')
            unit_code_erp = LocationMaster.objects.get(payroll_code=unit_code).erp_code

        grid = request.GET.get('grid', 'otdunitsummary')

        if grid == 'ontimedetail':
            sql_query = f"""EXEC [GET_SALE_TURNOVER] '{from_date_filt}', '{to_date_filt}', {f"'{unit_code_erp}'" if unit_code_erp else 'NULL'}, 'ontimedetail'"""
        elif grid == 'delaydetail':
            sql_query = f"""EXEC [GET_SALE_TURNOVER] '{from_date_filt}', '{to_date_filt}', {f"'{unit_code_erp}'" if unit_code_erp else 'NULL'}, 'delaydetail'"""
        else:
            sql_query = f"""EXEC [GET_SALE_TURNOVER] '{from_date_filt}', '{to_date_filt}', {f"'{unit_code_erp}'" if unit_code_erp else 'NULL'}, 'otdunitsummary'"""

        with connections['default'].cursor() as cursor:
            cursor.execute(sql_query)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        context = {
            'unit_code_erp': unit_code_erp,
            'unit_list': unit_list,
            'unit_code': unit_code,
            'from_date': from_date,
            'to_date': to_date,
            'from_date_filt': from_date_filt,
            'to_date_filt': to_date_filt,
            'data_list': data_list,
            'grid': grid
        }
        return render(request, 'on_time_delivery.html', context)
