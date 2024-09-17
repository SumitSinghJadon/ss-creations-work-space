from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from IS_Nexus.database.is_hrms import getYearMonthList ,get_payroll_db_name
from IS_Nexus.functions.data_conversion import queryset_to_json
from IntelliSync_db.models import CommonMaster,User
from datetime import datetime
from Payroll_db.models import EmployeeMaster
from django.db.models import F
import calendar



class TeamAttendanceView(View):
    def get(self,request):
        # try:
        emp_paycode=request.user.username
        usernames=User.objects.filter(reporting_manager=request.user.reporting_manager).values_list('username')

        team_paycodes = [username_tuple[0] for username_tuple in usernames]
        print('\n\n\n',usernames,'\n\n\n')
        # return HttpResponse(team_paycodes)
            # current_year=request.GET.get('year',datetime.now().year)
            # current_month = request.GET.get('month',datetime.now().month)
            # current_month2 = int(current_month)
            # year_list=getYearMonthList(emp_paycode)
            # month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('pk')
            # datetime_db=datetime(int(current_year),int(current_month),1)
            # current_month_k = datetime.now().month

            # if current_month2 < 4:
            #     if current_month2 in ['1', 1]:
            #         current_month2 = '13'

            #     elif current_month2 in ['2', 2]:
            #         current_month2 = '14'
                
            #     elif current_month2 in ['3', 3]:
            #         current_month2 = '15'
            # else:
            #     current_month2=current_month
            
            # days_in_month = calendar.monthrange(int(current_year), int(current_month))[1]

            # sum_ttl_hr=0
            # sum_lt_hr=0
            # sum_ery_hr=0
            # data=[]
            
            # raw_data=EmployeeMaster.objects.filter(time_master_emp_code__month_no=current_month2,time_hour_day_emp_code__month_no=current_month2,time_early_emp_code__month_no=current_month2).annotate(
            #     **{f'idt{i}': F(f'time_master_emp_code__idt{i}') for i in range(1, 32)},
            #     **{f'odt{i}': F(f'time_master_emp_code__odt{i}') for i in range(1, 32)},
            #     **{f'midt{i}': F(f'time_master_emp_code__midt{i}') for i in range(1, 32)},
            #     **{f'modt{i}': F(f'time_master_emp_code__modt{i}') for i in range(1, 32)},
            #     **{f'atp{i}': F(f'time_hour_day_emp_code__atp{i}') for i in range(1, 32)},
            #     **{f'ot{i}': F(f'time_hour_day_emp_code__ot{i}') for i in range(1, 32)},
            #     **{f'twm{i}': F(f'time_hour_day_emp_code__twm{i}') for i in range(1, 32)},
            #     **{f's{i}': F(f'time_hour_day_emp_code__s{i}') for i in range(1, 32)},
            #     **{f'lt{i}': F(f'time_hour_day_emp_code__lt{i}') for i in range(1, 32)},
            #     **{f'e{i}': F(f'time_early_emp_code__b{i}') for i in range(1, 32)}
            # ).values(
            #     'emp_code', 'emp_cardno', 'emp_name','emp_doj','resign', 
            #     *[f'idt{i}' for i in range(1, 32)],
            #     *[f'odt{i}' for i in range(1, 32)],
            #     *[f'midt{i}' for i in range(1, 32)],
            #     *[f'modt{i}' for i in range(1, 32)],
            #     *[f'atp{i}' for i in range(1, 32)],
            #     *[f'ot{i}' for i in range(1, 32)],
            #     *[f'twm{i}' for i in range(1, 32)],
            #     *[f's{i}' for i in range(1, 32)],
            #     *[f'lt{i}' for i in range(1, 32)],
            #     *[f'e{i}' for i in range(1, 32)]
            # ).order_by('emp_code').filter(emp_paycode=emp_paycode).using(get_payroll_db_name(datetime_db))

            # print('\n\n', raw_data.query, '\n\n')
            
            # month_abb=calendar.month_abbr[int(current_month)]
            
            # raw_data=queryset_to_json(raw_data)

            # if raw_data:
            #     for i in range(1,days_in_month+1):
            #         status_cls=""
            #         if str(raw_data[0][f'idt{i}']).strip()=='' or str(raw_data[0][f'odt{i}']).strip()=='':
            #             status_cls='!bg-amber-400'
            #         if str(raw_data[0][f'atp{i}']).strip()=='A-A':
            #             status_cls='!bg-red-400'
            #         elif str(raw_data[0][f'atp{i}']).strip() in ('P-A','A-P'):
            #             status_cls='!bg-red-200'
            #         elif str(raw_data[0][f'atp{i}']).strip()=='WO-WO':
            #             status_cls='!bg-amber-100'
                    
            #         date=f'0{i}-{month_abb}-{current_year}' if i<10 else f'{i}-{month_abb}-{current_year}'
            #         shift=raw_data[0][f's{i}']
            #         in_time=raw_data[0][f'idt{i}']
            #         m_in=str(raw_data[0][f'midt{i}']).strip()
            #         out=raw_data[0][f'odt{i}']
            #         m_out=str(raw_data[0][f'modt{i}']).strip()
            #         status=raw_data[0][f'atp{i}'].strip()
                    

            #         total_minutes = int(raw_data[0][f'twm{i}'])
            #         total_hours = f"{total_minutes // 60} hrs, {total_minutes % 60} mins" if total_minutes > 0 else ''
            #         sum_ttl_hr= sum_ttl_hr + total_minutes

            #         late_minutes = int(raw_data[0][f'lt{i}'])
            #         late_hours = f"{late_minutes // 60} hrs, {late_minutes % 60} mins" if late_minutes > 0 else ''

            #         early_minutes = int(raw_data[0][f'e{i}']) if int(raw_data[0][f'e{i}']) > 0 else 0
            #         early_hours = f"{early_minutes // 60} hrs, {early_minutes % 60} mins" if early_minutes > 0 else '' 
            #         if status.strip() == 'P-P':
            #             sum_lt_hr = sum_lt_hr + late_minutes
            #             sum_ery_hr = sum_ery_hr + early_minutes 
                    
            #         data.append({
            #             "date":date,
            #             "shift":shift,
            #             "in":in_time,
            #             "out":out,
            #             "m_in":m_in,
            #             "m_out":m_out,
            #             "total_hours":total_hours,
            #             "late_hours":late_hours,
            #             "early_hours":early_hours,
            #             "status":status,
            #             "css_cls":status_cls
            #         })

            # context={
            #     "year_list":year_list,
            #     "month_list":month_list,
            #     "current_year":str(current_year),
            #     "current_month":str(current_month),
            #     "range":range(1,days_in_month+1),
            #     "total_working_hours": f"{sum_ttl_hr // 60} hrs, {sum_ttl_hr % 60} mins",
            #     "total_late_hours":f"{sum_lt_hr // 60} hrs, {sum_lt_hr % 60} mins",
            #     "total_early_hours":f"{sum_ery_hr // 60} hrs, {sum_ery_hr % 60} mins",
            #     "data":data
            # }
        # except Exception as e:
        #     context = {}
        #     print("\n",e,"\n")
        return render(request,'teamAttendance.html',{})
    

        