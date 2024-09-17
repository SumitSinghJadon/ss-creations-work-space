from datetime import datetime
from pytz import timezone
from django.db import connections


def get_or_none(mdl, *args, **kwargs):
    try:
        return mdl.objects.get(*args, **kwargs)
    except mdl.DoesNotExist:
        return None


def get_next_number(mdl, prefix):
    try:
        next_no = mdl.objects.all().last()

        if not next_no:
            next_no = 1

        else:
            next_no = int(next_no.id) + 1
    
        curr_date = datetime.today().strftime('%d%m%y') 
        return f'{prefix}/{curr_date}/{next_no}'

    except mdl.DoesNotExist:
        return None
    

def get_auto_no(name=None, code=None):
    pass 


def update_auto_no(name=None, code=None, action='+'):
    pass 


def pay_db(date):
    from django.db import connections, connection
    cursor =  connections['default'].cursor()
    sql = f"""select db_name from is_app_db_new.dbo.unit_financial_year_mt where '{date}' between from_date and to_date """
    cursor.execute(sql)
    # samp_mt_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    data_arr = cursor.fetchone()
    return data_arr[0] if data_arr else None
    

def formate_date(date, formate='%Y-%m-%dT%H:%M'):
    if date:
        naive_expected_date = datetime.strptime(date, formate) 
        tz = timezone('Asia/Kolkata')
        aware_expected_date = tz.localize(naive_expected_date)
        return aware_expected_date

    return None


def execute_sql(database, query):
    cursor = connections[database].cursor()
    cursor.execute(query)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return data or None


def execute_sql_one(database, query):
    cursor = connections[database].cursor()
    cursor.execute(query)
    data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return data[0] if data else None

