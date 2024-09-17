from django.http import HttpResponse
from django.views import View
from IS_Nexus.functions import execute_sql
from IS_Nexus.database.is_hrms import get_payroll_db_name, hrms_mailer
from IntelliSync_db.models.user_master import User
from datetime import datetime
from django.template.loader import render_to_string

class HappyBdayMailer(View):
    def get(self,request):
        sql = """
            select emp_dob, emp_paycode, emp_name, dep.dep_name, loc.loc_name, des.des_name
            from tbemp emp
            join tbdep dep on emp.dep_code = dep.dep_code
            join tblocation loc on emp.loc_code = loc.loc_code
            join tbdes des on emp.des_code = des.des_code
            WHERE resign=0 and MONTH(emp_dob) = MONTH(GETDATE()) AND DAY(emp_dob) = DAY(GETDATE()) AND cat_code='4'
        """
        dob_data = execute_sql(get_payroll_db_name(datetime.now()), sql)
        if dob_data:
            for item in dob_data:
                try:
                    user=User.objects.get(username=item["emp_paycode"].strip())
                    # url='http://'+self.request.get_host()+"/static/images/Birthday-Cake-PNG-File.png"
                    url="https://clipart-library.com/image_gallery2/Birthday-Cake-PNG-File.png"
                
                    hrms_mailer(f'Happy Birthday { item["emp_name"] }',render_to_string('happy_bday_mail.html', {'data': item,'url':url}), user.email)
                except Exception as e:
                    print('\n\n',e,'\n\n')
            return HttpResponse("Done")
        return "some error occured"