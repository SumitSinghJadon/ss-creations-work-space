from django.views import View
from django.shortcuts import render
from IntelliSync_db.models import CommonMaster, FirstLevelMaster , SecondLevelMaster
from functions import delete_unused_stitch_temp_defect_trans , get_trans_srno_data , get_trans_srno_data_disp
from django.contrib import messages
from django.db import connection,connections
from datetime import datetime , timedelta


class DayEffView(View):
    def get(self, request):
        month = request.GET.get('month')
        year = request.GET.get('year')
        dayno = request.GET.get('dayno')
        
        if month and year:
            cursor = connections['default'].cursor()
            sql = f""" 
                EXEC GET_TAILOR_EFF '{month}','{year}','1',8,'tailor_day_eff','{dayno}'
            """
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()
        
        context ={
            'data_list' : data_list,
            'dayno' : dayno,
            'month' : month,
            'year' : year
        }
        return render(request, 'day_eff.html',context)
    