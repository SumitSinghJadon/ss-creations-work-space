from django.http import HttpResponse,JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages as msg
from django.db import connections, connection
from django.conf import settings
from django.core.mail import send_mail , EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from functions import sampling_mail_data , sys_para_val
from datetime import datetime , timedelta

class SendMailView(View):
    def get(self, request):
        curr_user = request.user.id
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']
        print(request.build_absolute_uri(),'\n\n')
        flag = request.GET.get('flag')

        
        if flag == 'test_mail': 
            pass
        elif flag == 'send_mail_sample_booking':
            # print('mail')
            email_from = settings.EMAIL_HOST_USER
            email_list = sys_para_val('SAMP_MAIL_MGNT')
            email_list_val = email_list[0]['email_list']
            # print(email_list_val)
            to_email = list(email_list_val.replace("'","").split(','))
            # print(to_email)
            # to_email = ['arjunkumar.223@gmail.com','developers@intellisync.in','implementation@ss-creations.in','implementation@intellisync.in','aryan@intellisync.in' ]
            # to_email = [ 'saurabh@globalfashionindia.com' ]
            subject = 'Sample Booking'
            html_template = 'sampling_mail.html'
            
            today_date = datetime.today().strftime('%Y-%m-%d')
            sql_size = f""" EXEC GET_SAMP_REPORTS 'sample_booking',NULL,NULL,NULL,NULL  """
            cursor=connections["default"].cursor()
            cursor.execute(sql_size)
            mail_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()
    
            # print(mail_data)
            # print(mail_data[0]['total_qty'])
            total =0
            for row in mail_data:
                i= row['total_qty']
                total = total + i

            # sum_col_1 = sum(mail_data[0]['total_qty'])
            context = { 'mail_data' : mail_data, 'sum_col_1' : total }
            html_message = render_to_string(html_template, context ) 

            message = EmailMessage(subject, html_message, email_from, to_email)
            message.content_subtype = 'html' # this is required because there is no plain text email message
            message.send()
            # return HttpResponse('Mail Send')
            return HttpResponse(html_message)
        
        elif flag == 'send_mail_sample_cost_old':
            # print('mail')
            email_from = settings.EMAIL_HOST_USER
            email_list = sys_para_val('SAMP_COST_MAIL_MGNT')
            email_list_val = email_list[0]['email_list']
            # print(email_list_val)
            to_email = list(email_list_val.replace("'","").split(','))
            # print(to_email)
            # to_email = ['arjunkumar.223@gmail.com','developers@intellisync.in','implementation@ss-creations.in','implementation@intellisync.in','aryan@intellisync.in' ]
            # to_email = [ 'saurabh@globalfashionindia.com' ]
            subject = 'Sample Cost'
            html_template = 'sampling_cost_mail2.html'
            today_date = datetime.today().strftime('%Y-%m-%d')
            curr_month = datetime.today().strftime('%m')
            curr_year = datetime.today().strftime('%Y')
            
            cursor = connections['is_app'].cursor()
            sql = f"""  select CONDIDTION from SystemParameters where ParameterName ='SAMP_DEPT' """
            cursor.execute(sql)
            dept_arr =  cursor.fetchone()
            cursor.close()
            dept = dept_arr[0]
            
            sql_size = f"""  EXEC GET_DAILY_MANP_LIST_DEPT_COST '{curr_month}','{curr_year}','1','{dept}','summ',NULL """
            cursor=connections["is_app"].cursor()
            cursor.execute(sql_size)
            mail_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()
            # print(mail_data)
            # print(mail_data[0]['total_qty'])
            total =0
            # for row in mail_data:
            #     i= row['total_qty']
            #     total = total + i
                            
            # sum_col_1 = sum(mail_data[0]['total_qty'])
            context = { 'mail_data' : mail_data, 'sum_col_1' : total }
            html_message = render_to_string(html_template, context ) 

            message = EmailMessage(subject, html_message, email_from, to_email)
            message.content_subtype = 'html' # this is required because there is no plain text email message
            message.send()
            # return HttpResponse('Mail Send')
            return HttpResponse(html_message)
        
        elif flag == 'send_mail_sample_cost':
            # print('mail')
            email_from = settings.EMAIL_HOST_USER
            email_list = sys_para_val('SAMP_COST_MAIL_MGNT')
            email_list_val = email_list[0]['email_list']
            # print(email_list_val)
            to_email = list(email_list_val.replace("'","").split(','))
            # print(to_email)
            # to_email = ['arjunkumar.223@gmail.com','developers@intellisync.in','implementation@ss-creations.in','implementation@intellisync.in','aryan@intellisync.in' ]
            # to_email = [ 'saurabh@globalfashionindia.com' ]
            
            html_template = 'sampling_cost_mail.html'
            # first_date = datetime.today().strftime('%Y-%m-%d')
            # today_date = datetime.today().strftime('%Y-%m-%d')

            first_date_disp = datetime.today().strftime('01-%m-%Y')
            today_date_disp = datetime.today().strftime('%d-%m-%Y')
            
            yesterday = datetime.now() - timedelta(days=1)
            prev_date = yesterday.strftime('%d-%m-%Y')

            curr_month = datetime.today().strftime('%m')
            curr_year = datetime.today().strftime('%Y')
            subject = f""" Sample Cost from {first_date_disp} To {prev_date}"""
            cursor = connections['is_app'].cursor()
            sql = f"""  select CONDIDTION from SystemParameters where ParameterName ='SAMP_DEPT' """
            cursor.execute(sql)
            dept_arr =  cursor.fetchone()
            cursor.close()
            dept = dept_arr[0]
            
            sql_size = f"""  EXEC GET_DAILY_MANP_LIST_DEPT_COST '{curr_month}','{curr_year}','1','{dept}','summ_cumm',NULL """
            cursor=connections["is_app"].cursor()
            cursor.execute(sql_size)
            mail_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()
            # print(mail_data)
            # print(mail_data[0]['total_qty'])
            total =0
            # for row in mail_data:
            #     i= row['total_qty']
            #     total = total + i
                            
            # sum_col_1 = sum(mail_data[0]['total_qty'])
            context = { 'mail_data' : mail_data, 'sum_col_1' : total, 'prev_date' : prev_date }
            html_message = render_to_string(html_template, context ) 

            message = EmailMessage(subject, html_message, email_from, to_email)
            message.content_subtype = 'html' # this is required because there is no plain text email message
            message.send()
            # return HttpResponse('Mail Send')
            return HttpResponse(html_message)

        elif flag == 'sample_closer':

            sql_size = f""" 
                update is_sampling_db.dbo.sample_booking_mt set is_active=0 where booking_no in  (
                select s.booking_no from is_sampling_db.dbo.sample_booking_mt (nolock) s
                left join (select booking_no,booking_id,sum(CAST(dispatch_qty as INT)) qty from is_sampling_db.dbo.dispatch_entry_mt (nolock) group by booking_no,booking_id) d on s.id = d.booking_id 
                where s.total_qty = d.qty
) 
                """
            cursor=connections["is_app"].cursor()
            cursor.execute(sql_size)
            cursor.close()

            return HttpResponse('Done')
        
        return HttpResponse('Error')    

