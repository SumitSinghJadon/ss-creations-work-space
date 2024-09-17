from IntelliSync_db.models import CommonMaster, FirstLevelMaster
from IS_Nexus.functions import queryset_to_json
from ERP_db.models import *
from django.db import connections, connection

# Fetch all merchants from first level master based on merchant head preset in common master
def get_merchant_by_merchant_head(mid, **kwargs):
    try:
        fields = kwargs.get('fields', []) 
        merchant_head = CommonMaster.objects.get(master_type__code='CT-22', id=mid, is_active=True)
        data_list = FirstLevelMaster.objects.filter(master_type__code='CT-23', is_active=True, common_master=merchant_head).values(*fields)
        return queryset_to_json(data_list)
    
    except Exception as e:
        print(e)
        return None 


# def get_style_by_buyer(bid, **kwargs):
#     try:
#         fields = kwargs.get('fields', []) 
#         data_list = Style.objects.filter(locked=1, buyer=bid).values(*fields)
#         return queryset_to_json(data_list) 

#     except Exception as e:
#         print(e)
#         return None

def get_style_by_buyer(buyer, **kwargs):
    cursor =  connections['erp_db'].cursor()
    sql = f"""
    select e.styleno 
    from  ExpoLotDet E
    join Expohead s on E.ourref = s.ourref
    join Style ss ON e.styleno = ss.styleno
    join Party P ON s.buyer = p.party_code
    where p.party_code  ='{buyer}'
    group by e.styleno order by e.styleno asc
    """
    cursor.execute(sql)
    style_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    # style_list = style_list[0] if style_list else None
    # print(samp_mt_data)
    cursor.close()
    return style_list

def get_season_year_by_season(sid, **kwargs):
    try:
        fields = kwargs.get('fields', []) 
        sid = CommonMaster.objects.get(master_type__code='CT-12', id=sid, is_active=True)
        data_list = FirstLevelMaster.objects.filter(master_type__code='CT-13', is_active=True, common_master=sid).values(*fields)
        return queryset_to_json(data_list)

    except Exception as e:
        print(e)
        return None

