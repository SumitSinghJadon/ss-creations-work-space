from django.db import connections
from datetime import datetime


current_year=int(datetime.now().strftime("%y"))
current_year_list=[current_year-2,current_year-1,current_year]
def get_payroll_db():
    sql = 'select * from '


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
    cursor = connections['payroll_db'].cursor()
    sql = f"""select * from tbdep (nolock) d order by dep_name asc """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 


def get_desg_list():
    cursor = connections['payroll_db'].cursor()
    sql = f"""select * from tbdes (nolock) d order by des_name asc """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_dept_desg_list(unit_code=None):
    cursor = connections['payroll_db'].cursor()
    sql = f"""
        select d.dep_code,d.dep_name,ds.des_code,ds.des_name,count(e.emp_code) onroll ,m.manpower as app_manp,m.id as app_id
        from tbemp (nolock) e 
        join tbdep (nolock) d on e.dep_code = d.dep_code 
        join tbdes (nolock) ds on e.des_code = ds.des_code
        left join [IS_KPI_DB].[dbo].[manpower_plan] m on e.dep_code = m.department and e.des_code = m.designation
        where e.resign=0
        group by d.dep_code,d.dep_name,ds.des_code,ds.des_name ,m.manpower,m.id
        order by d.dep_name,ds.des_name asc
    """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_dept_desg_hr_list(unit_code=None):
    cursor = connections['payroll_db'].cursor()
    sql = f"""
        select d.dep_code,d.dep_name,ds.des_code,ds.des_name,count(e.emp_code) onroll ,m.manpower as app_manp,m2.id as app_id,m2.remarks
        from tbemp (nolock) e 
        join tbdep (nolock) d on e.dep_code = d.dep_code 
        join tbdes (nolock) ds on e.des_code = ds.des_code
        left join [IS_KPI_DB].[dbo].[manpower_plan] m on e.dep_code = m.department and e.des_code = m.designation
        left join [IS_KPI_DB].[dbo].[manpower_hr] m2 on e.dep_code = m2.department and e.des_code = m2.designation
        where e.resign=0
        group by d.dep_code,d.dep_name,ds.des_code,ds.des_name ,m.manpower,m2.id,m2.remarks
        order by d.dep_name,ds.des_name asc
    """
    cursor.execute(sql)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return data 

def get_manpower_plan_data(dept,desg,unit=1):
    cursor = connections['default'].cursor()
    sql = f"""select manpower from manpower_plan where department ='{dept}' and designation ='{desg}' """
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
            EXEC GET_PAYROLL_DATA '{month}','{year}','{unit_code}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def get_staff_worker_today_list(month=None,year=None,unit_code=None):
    if month and year and unit_code:
        cursor =  connections['default'].cursor()
        sql = f""" 
            EXEC GET_STAFF_WORKER_SUMMARY '{month}','{year}','{unit_code}'
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