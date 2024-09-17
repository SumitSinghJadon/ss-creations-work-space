from django.views import View
from django.shortcuts import render , redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster , SecondLevelMaster
from functions import delete_unused_stitch_temp_defect_trans , get_trans_srno_data , get_trans_srno_data_disp
from django.contrib import messages
from django.db import connection,connections
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db

class SampleTransReportView(View):
    def get(self, request):
        booking_id = request.GET.get('booking_id')
        
        if request.GET.get('from_date') and request.GET.get('to_date'):
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
        else:
             from_date = datetime.today().strftime('%Y-%m-01')
             to_date = datetime.today().strftime('%Y-%m-%d')
        
        if request.GET.get('process'):
            process = request.GET.get('process')
        else:
            process = None
            
        if request.GET.get('style'):
            style = request.GET.get('style')
        else:
            style = None
            
        data_list =[]
        if from_date and to_date and process:
            cursor =  connections['default'].cursor()
            
            sql_cutter1 = f""" EXEC GET_SAMP_TRANSACTION '{from_date}','{to_date}', """
            
            if request.GET.get('process'):
                process = request.GET.get('process')
                sql_cutter2 = f""" '{process}', """
            else:
                sql_cutter2 = f""" NULL, """
            
            if request.GET.get('buyer'):
                buyer = request.GET.get('buyer')
                sql_cutter3 = f""" '{buyer}', """
            else:
                sql_cutter3 = f""" NULL, """

            if request.GET.get('merchant'):
                merchant = request.GET.get('merchant')
                sql_cutter4 = f""" '{merchant}', """
            else:
                sql_cutter4 = f""" NULL, """

            if request.GET.get('sample_dept'):
                sample_dept = request.GET.get('sample_dept')
                sql_cutter5 = f""" '{sample_dept}' """
            else:
                sql_cutter5 = f""" NULL """

            sql_cutter = sql_cutter1 + sql_cutter2 + sql_cutter3 + sql_cutter4 + sql_cutter5
            # print(sql_cutter)
            cursor.execute(sql_cutter)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            data_list[0] if data_list else None
        # print(data_list)
        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)
        
        cursor =  connections['default'].cursor()
        sql_cutter = f""" select dep_code,dep_name from {db_name}.dbo.tbdep where dep_code in ( SELECT CAST(Item AS INTEGER) FROM is_app_db_new.dbo.split((select CONDIDTION from is_app_db_new.dbo.SystemParameters where ParameterName = 'SAMP_DEPT' ), ',') ) """
        cursor.execute(sql_cutter)
        samp_dept_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        samp_buyer = []
        
        context ={
            'booking_id' : booking_id,
            'data_list' : data_list,
            'samp_dept_list' : samp_dept_list,
            'samp_buyer' : samp_buyer,
            'from_date' : from_date,
            'to_date' : to_date,
            'process' : process,
            'style' : style,
        }
        return render(request, 'sample_trans_report.html',context)

    