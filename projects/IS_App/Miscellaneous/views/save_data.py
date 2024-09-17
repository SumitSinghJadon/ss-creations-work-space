from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages as msg
from IS_Nexus.functions import messages,queryset_to_json
from django.db import connections, connection
from django.conf import settings
import json

class SaveDataView(View):
    def get(self, request):
        created_by = request.user.id
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']
        print(request.build_absolute_uri(),'\n\n')
        flag = request.GET.get('flag')
        created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        # print(flag)
        if flag == 'manpower_alloc':
            # emp_name_list     = request.GET.getlist('emp_name')
            counter     = request.GET.get('counter')
            # print(counter)
            dayno        =request.GET.get('dayno')
            unit_code    =request.GET.get('unit_code')
            emp_code     =request.GET.get('emp_code')
            emp_name     =request.GET.get('emp_name')
            line_type    =request.GET.get('line_type')
            line_name    =request.GET.get('line_name')
            ot_line      =request.GET.get('ot_line')

            # print(dayno,unit_code,emp_code,emp_name,line_type,line_name,ot_line)
            # print('\n')

            cursor =  connections['default'].cursor()
            sql = f"""  select count(*) cont from is_app_db_new.dbo.manpower_alloc where dayno ='{dayno}' and emp_code = '{emp_code}'  """
            cursor.execute(sql)
            chk_data = cursor.fetchone()
            # print(chk_data)
            if chk_data[0] == 0:
                sql_ins = f"""  insert into is_app_db_new.dbo.manpower_alloc(unit_code,dayno,emp_code,emp_name,line_type,line_code,style_no,order_no,ot_line,is_active,created_at,updated_at,created_by,updated_by) values('{unit_code}','{dayno}','{emp_code}','{emp_name}','{line_type}','{line_name}','','','{ot_line}','1','{created_at}','{created_at}','{created_by}','{created_by}')  """
            else:
                sql_ins = f"""  update is_app_db_new.dbo.manpower_alloc set line_type='{line_type}',line_code='{line_name}',ot_line='{ot_line}',updated_by='{created_by}',updated_at='{created_at}' where dayno ='{dayno}' and emp_code = '{emp_code}'  """
            
            # print(sql_ins)
            sql_d = cursor.execute(sql_ins)
            cursor.close()
            # sql_d= 1
            if sql_d:
                return HttpResponse(1)
            else:
                return HttpResponse(0)

        return HttpResponse('Data Not Saved')
