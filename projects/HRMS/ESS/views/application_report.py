from django.views import View
from django.shortcuts import render
from IntelliSync_db.models import CommonMaster, User
from HRMS_db.models import LeaveApplication
from IS_Nexus.functions.shortcuts import formate_date, execute_sql,pay_db
from IS_Nexus.database.is_hrms import get_payroll_db_name
from django.db.models import Q
from datetime import date,datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse


class ApplicationReport(View):
    def get(self, request):
        if use := request.GET.get('use'):
            today_date=date.today()
            
            subject = 'Daily Application Report'
            email_from = 'implementation@ss-creations.in'
            recipient_list = ['sharmashantum@mgail.com',"developers@intellisync.in"]

            db_name=pay_db(today_date)
            sql = f"""
                select t2.username, emp.emp_name, dep.dep_name, loc.loc_name, des.des_name, t1.application_type, t1.from_date, t1.till_date,t1.day_count, t1.reason, t1.status, t1.leave_type from [IS_HRIMS_db].[dbo].[application] t1 JOIN [k_intellisync_db].[dbo].user_master t2 on t2.id= t1.user_id JOIN tbemp emp on emp.emp_paycode = t2.username JOIN tbdep dep ON emp.dep_code = dep.dep_code JOIN tblocation loc ON emp.loc_code = loc.loc_code JOIN tbdes des ON emp.des_code = des.des_code WHERE CONVERT(date, applied_on) = CONVERT(date, GETDATE())
            """
            application_list = execute_sql(get_payroll_db_name(datetime.now()), sql)
            html_content = render_to_string('dailyReportMail.html', {'application_list': application_list})
            text_content = strip_tags(html_content)
            try:
                # Create the email message
                msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
                msg.attach_alternative(html_content, "text/html")  # Attach HTML content

                # Send the email
                msg.send()
                return HttpResponse('Email sent successfully!')
            except Exception as e:
                return HttpResponse('Failed to send email. Error: {}'.format(str(e)))
            

        else:
            user_list   = User.objects.using('intellisync_db').all().filter(is_active=True)
            year_list   = CommonMaster.objects.filter(master_type__code='CT-20').values('name', 'value').order_by('-name')
            month_list  = CommonMaster.get_month_list()

            eid = request.GET.get('eid')
            from_date = request.GET.get('from_date')
            till_date = request.GET.get('till_date')
            status = request.GET.get('status')

            application_list = LeaveApplication.objects.all()
            combined_filters = None
            if eid or from_date or till_date or status:
                combined_filters = Q()

            if eid:
                combined_filters &= Q(user=eid)

            if from_date:
                from_date = formate_date(f"{from_date}T00:00")
                combined_filters &= Q(from_date__gte=from_date)

            if till_date:
                till_date = formate_date(f"{till_date}T00:00")
                combined_filters &= Q(till_date__lte=till_date)

            if status:
                combined_filters &= Q(status=status)

            if combined_filters != None:
                application_list = application_list.filter(combined_filters)

            context = {
                'user_list'       : user_list,
                'year_list'       : year_list,
                'month_list'      : month_list,
                'application_list': application_list
            }

            return render(request,"applicationReport.html",context)



