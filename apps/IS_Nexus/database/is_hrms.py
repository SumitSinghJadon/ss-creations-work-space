from datetime import datetime, timedelta
from IS_Nexus.functions.data_conversion import queryset_to_json
from Payroll_db.models import EmployeeMaster
from IntelliSync_db.models import CommonMaster,User,LocationMaster
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def get_payroll_db_name(date):
    current_year = date.year
    if date.month < 4:
        current_year -= 1
    return f'payroll_db_{str(current_year)[-2:]}'

def getEmployeeDetails(emp_paycode):
    date=datetime.now().strftime('%Y-%m-%d')
    data=EmployeeMaster.objects.filter(emp_paycode=emp_paycode).values('emp_code','emp_paycode','emp_name','loc_code','dep_code','dep_code__dep_name','emp_doj', 'emp_phn').using(get_payroll_db_name(datetime.now()))
    rpr=User.objects.filter(username=emp_paycode).values('reporting_manager')
    
    reporting_person={}
    if rpr.exists():
        for item in rpr:
            reporting_person["emp_paycode"]=item["reporting_manager"]
        rpr=User.objects.filter(pk=reporting_person["emp_paycode"]).values('full_name')
        for item in rpr:
            reporting_person["emp_name"]=item["full_name"]
    else: 
        reporting_person["emp_paycode"]=""
        reporting_person["emp_name"]=""
    
    arr={}

    for item in data:
        arr["emp_code"]=item["emp_code"]
        arr["dep_code"]=item["dep_code"]
        arr["emp_paycode"]=str(item["emp_paycode"]).strip()
        arr["emp_name"]=str(item["emp_name"]).strip()
        arr["loc_code"]=str(item["loc_code"]).strip()
        loc_name = LocationMaster.objects.get(payroll_code=arr["loc_code"])
        arr["loc_name"]=loc_name.name
        arr["dep_name"]=str(item["dep_code__dep_name"]).strip()
        arr["joining_date"]=item["emp_doj"]
        arr["reporting_manager"]=reporting_person
        
    context={
        "date":date,
        "data":arr
    }
    
    return context

def getYearMonthList(emp_paycode):
    date=datetime.now()
    data=EmployeeMaster.objects.filter(emp_paycode=emp_paycode).values('emp_doj').using(get_payroll_db_name(date))
    doj=''
    for item in data:
        doj=item["emp_doj"]
    
    year=doj.year if doj.year>=2024 else 2024
    year_list=queryset_to_json(CommonMaster.objects.filter(master_type__code='CT-20').values_list('name').order_by('-name'))
    year_list=[item for items in year_list for item in items if int(item)>=year]
    return year_list
    
def getSundays():
    today = datetime.now()
    sundays = []
    year = today.year
    date = datetime(year, 1, 1)
    while date <= today:
        if date.weekday() == 6:  # Sunday has index 6
            sundays.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)
    return sundays


def hrms_mailer(subject,mail_content,recipient_list):
    email_from = 'implementation@ss-creations.in'
    msg = EmailMultiAlternatives(subject, strip_tags(mail_content), email_from, recipient_list)
    msg.attach_alternative(mail_content, "text/html")
    msg.send()
