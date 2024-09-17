from django.db import connections, connection
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from Payroll_db.models import EmployeeMaster
from App_db.models import MmrMT

def get_employee_list():
    data = [{'name':'arjun','age':34},{'name':'Abhay','age':24}]
    return data

def get_unit_list():
    cursor = connections['is_main_db'].cursor()
    sql = f"""select * from location_master (nolock) d order by name asc """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_dep_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor = connections['default'].cursor()
    sql = f"""select * from {db_name}.dbo.tbdep (nolock) d order by dep_name asc """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_desg_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor = connections['default'].cursor()
    sql = f"""select * from {db_name}.dbo.tbdes (nolock) d order by des_name asc """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_dept_desg_list(dayno,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_MMR_DEPT_DESG_DATA '{dayno}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def get_dept_desg_hr_list(dayno,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_MMR_DEPT_DESG_HR_DATA '{dayno}', '{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def get_dept_desg_hr_summ(dayno,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_MMR_DEPT_DESG_HR_SUMM '{dayno}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def get_present_tailor(dayno,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_TOTAL_PRESENT_TAILOR '{dayno}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def get_daily_manpower_list(month=None,year=None,unit_code=None):
    if month and year and unit_code:
        cursor =  connections['default'].cursor()
        sql = f""" 
            EXEC GET_DAILY_MANP_SUMMARY '{month}','{year}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []   

def get_manpower_plan_data(dept,desg,unit=1):
    cursor = connections['default'].cursor()
    sql = f"""select isnull(manpower,0) manpower from manpower_plan where department ='{dept}' and designation ='{desg}' """
    cursor.execute(sql)
    #data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    data = cursor.fetchone()
    return  (data[0] if data else None)

def get_mmr_list(unit_code):
    cursor =  connections['default'].cursor()
    sql = f""" select * from mmr_mt where unit_code='{unit_code}' order by from_date,to_date desc """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_month_punch_list(month=None,year=None,unit_code=None):
    if month and year and unit_code:
        cursor =  connections['default'].cursor()
        sql = f""" 
            EXEC GET_payroll_db_DATA '{month}','{year}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_staff_worker_today_list(prev_date,today_date,month=None,year=None,unit_code=None):
    if prev_date and today_date and month and year and unit_code:
        cursor =  connections['default'].cursor()
        sql = f""" 
            EXEC GET_STAFF_WORKER_SUMMARY '{prev_date}','{today_date}','{month}','{year}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_staff_worker_attr_list(month=None,year=None,unit_code=None):
    if month and year and unit_code:
        cursor =  connections['default'].cursor()
        sql = f""" 
            EXEC GET_STAFF_WORKER_ATTR_SUMMARY '{month}','{year}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_emp_list(dayno,department,designation=None,unit_code=None):
    if dayno and department and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_EMP_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_emp_view_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_EMP_VIEW_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_gm_pending_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_GM_PENDING_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_gm_approve_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_GM_APPROVE_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_gm_reject_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_GM_REJECT_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_head_pending_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_HEAD_PENDING_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def get_ot_head_approve_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_HEAD_APPROVE_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_head_reject_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_HEAD_REJECT_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_unauth_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_UNAUTH_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_approve_excess_list(dayno,department=None,designation=None,unit_code=None):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_APPROVE_EXCESS_DATA '{dayno}','{department}','{designation}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_ot_master_list(dayno,unit_code):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_OT_MASTER_DATA '{dayno}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []

def get_unit_dept_list(dayno,unit_code):
    if dayno and unit_code:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_UNIT_DEPARTMENT_DATA '{dayno}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return []  

def get_erp_trans_data(dayno,process,unit_code=None):
    if dayno and process:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_CUTTING_DATA_ERP '{dayno}','8','{process}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def create_mmr(unit_code,dayno):
    # cursor = connections['default'].cursor()
    # sql = """ select max() from mmr_mt """
    max_no = MmrMT.objects.all().values("id").last()
    if not max_no:
        max_no =1
    else:
        max_no = int(max_no['id']) + 1

    prev_date = datetime.today().strftime('%d%m%y') 
    to_date = datetime.today().strftime('2999-%m-%d') 
    curr_date = datetime.today().strftime('%Y-%m-%d') 

    cursor = connections['default'].cursor()
    sql = f"""  
    select mmr_code,( select COUNT(*) from manpower_plan where mmr_code = m.mmr_code) plan_count from mmr_mt m where '{dayno}' between from_date and to_date 
    and to_date > convert(varchar,getdate(),23)  
    and unit_code ='{unit_code}'
    """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    if data:
        mmr_code = data[0]['mmr_code']
        cursor = connections['default'].cursor()
        sql = f""" update mmr_mt set to_date='{curr_date}' where mmr_code = '{mmr_code}' """
        cursor.execute(sql)
        plan_count = data[0]['plan_count']
    else:
        mmr_code = f"MMR/{prev_date}/{max_no}"
        plan_count = 0

    if unit_code and dayno and plan_count == 0:
        MmrMT.objects.create(
            mmr_code=mmr_code,
            unit_code=unit_code,
            from_date=dayno,
            to_date=to_date
        )
        error = 0
    else:
        error =1
        
    cursor = connections['default'].cursor()
    sql = f""" select mmr_code,from_date,to_date from mmr_mt  where mmr_code = '{mmr_code}' """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    if data:
        from_date = data[0]['from_date']
        to_date = data[0]['to_date']
    else:
        from_date = dayno
        to_date = to_date
    
    return mmr_code,from_date,to_date,error
