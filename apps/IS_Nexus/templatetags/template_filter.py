from django import template
from django.db import connections

register = template.Library()

@register.filter(name='get_buyer_name')
def get_buyer_name(buyer_code):
    cursor = connections['erp_db'].cursor()
    sql = f'''
        SELECT DISTINCT t2.party_code as buyer_code, t2.party_name as buyer_name
        FROM expohead t1
        JOIN party t2 ON t1.buyer = t2.party_code
        WHERE t2.party_code = '{buyer_code}'
    '''
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    if row:
        return row[1] 
    else:
        return None  

