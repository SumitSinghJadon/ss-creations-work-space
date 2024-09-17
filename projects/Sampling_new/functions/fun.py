from django.db import connections, connection
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from django.conf import settings

intellisync_db = settings.DATABASES['intellisync_db']['NAME']

def delete_unused_stitch_temp_trans(bid):
    cursor =  connections['default'].cursor()
    sql = f""" delete from transaction_entry_mt where booking_id ='{bid}' and trans_type='stitch' """
    cursor.execute(sql)
    cursor.close()

def delete_unused_finish_temp_trans(bid):
    cursor =  connections['default'].cursor()
    sql = f""" delete from transaction_entry_mt where booking_id ='{bid}' and trans_type='finish' """
    cursor.execute(sql)
    cursor.close()

def delete_unused_dispatch_temp_trans(bid):
    cursor =  connections['default'].cursor()
    sql = f""" delete from transaction_entry_mt where booking_id ='{bid}' and trans_type='dispatch' """
    cursor.execute(sql)
    cursor.close()

def delete_unused_stitch_temp_defect_trans(trans_id):
    cursor =  connections['default'].cursor()
    sql = f""" delete from defect_transaction_entry_mt where trans_id ='{trans_id}' and trans_type='stitch' """
    cursor.execute(sql)
    cursor.close()

def delete_unused_finish_temp_defect_trans(trans_id):
    cursor =  connections['default'].cursor()
    sql = f""" delete from defect_transaction_entry_mt where trans_id ='{trans_id}' and trans_type='finish' """
    cursor.execute(sql)
    cursor.close()

def delete_unused_dispatch_temp_defect_trans(trans_id):
    cursor =  connections['default'].cursor()
    sql = f""" delete from defect_transaction_entry_mt where trans_id ='{trans_id}' and trans_type='dispatch' """
    cursor.execute(sql)
    cursor.close()

    
def samp_booking_data(bid):
    cursor =  connections['default'].cursor()
    sql = f""" 
    select booking_no,booking_type,
    (CASE WHEN S.booking_type= 'F' THEN 'Fresh' WHEN S.booking_type= 'A' THEN 'Alter' WHEN S.booking_type= 'R' THEN 'Resubmission' END) booking_type_name,
    C3.name as sample_type,
    merchant_head_id,C1.name as merchant_head_name,merchant_name_id,C2.name as merchant_name,buyer_name,sample_type_id,
    style_no,season_year_id,C6.name as season_year,season_id,C4.name as season,booking_date,target_date,product_type_id,C5.name as product_type, 
    (select sum(quantity) samp_qty from sample_size_quantity where booking_id_id = s.id) samp_qty,
    STUFF((SELECT ','+ CAST(t.size as VARCHAR) FROM sample_size_quantity t WHERE booking_id_id= s.id  FOR XML PATH('')), 1, 1, '') sizes,
    c.qty as cut_qty,s.cut_assign_date,s.stitch_assign_date,s.finish_assign_date, s.dispatch_assign_date

    from sample_booking_mt  s
    JOIN ( SELECT cm.id, cm.master_type_id, cm.name, cm.value, cm.code, cm.remark, cm.other, cm.is_active FROM {intellisync_db}.dbo.common_master cm INNER JOIN {intellisync_db}.dbo.common_master_type cmt ON (cm.master_type_id = cmt.id)  WHERE cm.is_active = 'True'  ) C1 ON C1.id = s.merchant_head_id
    JOIN (  select id,name from {intellisync_db}.dbo.first_level_master ) C2 ON C2.id = s.merchant_name_id
    JOIN (  select id,name from {intellisync_db}.dbo.first_level_master ) C3 ON C3.id = s.sample_type_id
    JOIN ( SELECT cm.id, cm.master_type_id, cm.name, cm.value, cm.code, cm.remark, cm.other, cm.is_active FROM {intellisync_db}.dbo.common_master cm INNER JOIN {intellisync_db}.dbo.common_master_type cmt ON (cm.master_type_id = cmt.id)  WHERE cm.is_active = 'True'  ) C4 ON C4.id = s.season_id
    JOIN ( SELECT cm.id, cm.master_type_id, cm.name, cm.value, cm.code, cm.remark, cm.other, cm.is_active FROM {intellisync_db}.dbo.common_master cm INNER JOIN {intellisync_db}.dbo.common_master_type cmt ON (cm.master_type_id = cmt.id)  WHERE cm.is_active = 'True'  ) C5 ON C5.id = s.product_type_id
    JOIN (  select id,name from {intellisync_db}.dbo.first_level_master ) C6 ON C6.id = s.season_year_id
    left join (select booking_id,SUM(qty) qty from stitch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id )  c on s.id  =c.booking_id

    where s.id ='{bid}' """
    cursor.execute(sql)
    samp_mt_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    samp_mt_data = samp_mt_data[0] if samp_mt_data else None
    # print(samp_mt_data)
    cursor.close()
    return samp_mt_data

def trans_sample_size_color_wise_qty(bid):
    sql_size = f"""
        select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
        ISNULL(c.qty,0) as total_cut_qty , ISNULL(( sum(s.quantity) - ISNULL(c.qty,0) ),0) balance_cut_qty,
        ISNULL(tra.qty,0) trans_cutting_qty, ISNULL(tra.id,0) as tra_id
        from sample_size_quantity (nolock) s 
        left join (select booking_id,size,color,SUM(qty) qty from cutting_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
        left join (select id,booking_id,size,color,SUM(qty) qty from transaction_entry_mt (nolock) where booking_id = '{bid}' and trans_type='cutting' group by id,booking_id,size,color )  tra on s.booking_id_id  =tra.booking_id and s.size = tra.size and s.color = tra.color

        where s.booking_id_id = '{bid}' and s.is_active='1'
        group by s.booking_id_id,s.size,s.color,c.qty,tra.qty,tra.id 
        order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data


def trans_other_size_color_wise_qty(bid):
    sql_size = f"""
        select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
        ISNULL(c.qty,0) as total_cut_qty , ISNULL(( sum(s.quantity) - ISNULL(c.qty,0) ),0) balance_cut_qty,
        ISNULL(tra.qty,0) trans_cutting_qty, ISNULL(tra.id,0) as tra_id
        from sample_size_quantity (nolock) s 
        left join (select booking_id,size,color,SUM(qty) qty from other_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
        left join (select id,booking_id,size,color,SUM(qty) qty from transaction_entry_mt (nolock) where booking_id = '{bid}' and trans_type='other' group by id,booking_id,size,color )  tra on s.booking_id_id  =tra.booking_id and s.size = tra.size and s.color = tra.color

        where s.booking_id_id = '{bid}' and s.is_active='1'
        group by s.booking_id_id,s.size,s.color,c.qty,tra.qty,tra.id 
        order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def sample_size_color_wise_qty(bid):
    sql_size = f"""
        select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
        ISNULL(c.qty,0) as total_cut_qty , ISNULL(( sum(s.quantity) - ISNULL(c.qty,0) ),0) balance_cut_qty
        from sample_size_quantity (nolock) s 
        left join (select booking_id,size,color,SUM(qty) qty from cutting_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
        where s.booking_id_id = '{bid}' and s.is_active='1'
        group by s.booking_id_id,s.size,s.color,c.qty 
        order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def trans_cutting_size_color_wise_qty(bid):
    sql_size = f"""
    select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
    ISNULL(c.qty,0) as total_cut_qty ,ISNULL(st.qty,0) total_stitch_qty, ISNULL( (ISNULL(c.qty,0) - ISNULL(st.qty,0) ),0) balance_stitch_qty,
    ISNULL(tra.qty,0) trans_stitch_qty, ISNULL(tra.id,0) as tra_id
    from sample_size_quantity (nolock) s 
    join (select booking_id,size,color,SUM(qty) qty from cutting_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
    left join (select booking_id,size,color,SUM(qty) qty from stitch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s.booking_id_id  =st.booking_id and s.size = st.size and s.color = st.color
    left join (select id,booking_id,size,color,SUM(qty) qty from transaction_entry_mt (nolock) where booking_id = '{bid}' and trans_type='stitch' group by id,booking_id,size,color )  tra on s.booking_id_id  =tra.booking_id and s.size = tra.size and s.color = tra.color

    where s.booking_id_id = '{bid}' and s.is_active='1'
    group by s.booking_id_id,s.size,s.color,c.qty,st.qty,tra.qty,tra.id 
    order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def cutting_size_color_wise_qty(bid):
    sql_size = f"""
    select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
    ISNULL(c.qty,0) as total_cut_qty ,ISNULL(st.qty,0) total_stitch_qty, ISNULL( (ISNULL(c.qty,0) - ISNULL(st.qty,0) ),0) balance_stitch_qty
    from sample_size_quantity (nolock) s 
    join (select booking_id,size,color,SUM(qty) qty from cutting_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
    left join (select booking_id,size,color,SUM(qty) qty from stitch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s.booking_id_id  =st.booking_id and s.size = st.size and s.color = st.color
    where s.booking_id_id = '{bid}' and s.is_active='1'
    group by s.booking_id_id,s.size,s.color,c.qty,st.qty 
    order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def trans_stitching_size_color_wise_qty(bid):
    sql_size = f"""
    select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
    ISNULL(c.qty,0) as total_stitch_qty ,ISNULL(st.qty,0) total_finish_qty, ISNULL( (ISNULL(c.qty,0) - ISNULL(st.qty,0) ),0) balance_finish_qty,
    ISNULL(tra.qty,0) trans_finish_qty, ISNULL(tra.id,0) as tra_id
    from sample_size_quantity (nolock) s 
    join (select booking_id,size,color,SUM(qty) qty from stitch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
    left join (select booking_id,size,color,SUM(qty) qty from finish_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s.booking_id_id  =st.booking_id and s.size = st.size and s.color = st.color
    left join (select id,booking_id,size,color,SUM(qty) qty from transaction_entry_mt (nolock) where booking_id = '{bid}' and trans_type='finish' group by id,booking_id,size,color )  tra on s.booking_id_id  =tra.booking_id and s.size = tra.size and s.color = tra.color

    where s.booking_id_id = '{bid}' and s.is_active='1'
    group by s.booking_id_id,s.size,s.color,c.qty,st.qty,tra.qty,tra.id 
    order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def stitching_size_color_wise_qty(bid):
    sql_size = f"""
    select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
    ISNULL(c.qty,0) as total_stitch_qty ,ISNULL(st.qty,0) total_finish_qty, ISNULL( (ISNULL(c.qty,0) - ISNULL(st.qty,0) ),0) balance_finish_qty
    from sample_size_quantity (nolock) s 
    join (select booking_id,size,color,SUM(qty) qty from stitch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
    left join (select booking_id,size,color,SUM(qty) qty from finish_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s.booking_id_id  =st.booking_id and s.size = st.size and s.color = st.color
    where s.booking_id_id = '{bid}' and s.is_active='1'
    group by s.booking_id_id,s.size,s.color,c.qty,st.qty 
    order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def trans_finishing_size_color_wise_qty(bid):
    sql_size = f"""
    select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
    ISNULL(c.qty,0) as total_finish_qty ,ISNULL(st.qty,0) total_dispatch_qty, ISNULL( (ISNULL(c.qty,0) - ISNULL(st.qty,0) ),0) balance_dispatch_qty,
    ISNULL(tra.qty,0) trans_dispatch_qty, ISNULL(tra.id,0) as tra_id
    from sample_size_quantity (nolock) s 
    join (select booking_id,size,color,SUM(qty) qty from finish_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
    left join (select booking_id,size,color,SUM(qty) qty from dispatch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s.booking_id_id  =st.booking_id and s.size = st.size and s.color = st.color
    left join (select id,booking_id,size,color,SUM(qty) qty from transaction_entry_mt (nolock) where booking_id = '{bid}' and trans_type='dispatch' group by id,booking_id,size,color )  tra on s.booking_id_id  =tra.booking_id and s.size = tra.size and s.color = tra.color

    where s.booking_id_id = '{bid}' and s.is_active='1'
    group by s.booking_id_id,s.size,s.color,c.qty,st.qty,tra.qty,tra.id 
    order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def finishing_size_color_wise_qty(bid):
    sql_size = f"""
    select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
    ISNULL(c.qty,0) as total_finish_qty ,ISNULL(st.qty,0) total_dispatch_qty, ISNULL( (ISNULL(c.qty,0) - ISNULL(st.qty,0) ),0) balance_dispatch_qty
    from sample_size_quantity (nolock) s 
    join (select booking_id,size,color,SUM(qty) qty from finish_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
    left join (select booking_id,size,color,SUM(qty) qty from dispatch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s.booking_id_id  =st.booking_id and s.size = st.size and s.color = st.color
    where s.booking_id_id = '{bid}' and s.is_active='1'
    group by s.booking_id_id,s.size,s.color,c.qty,st.qty 
    order by s.size,s.color asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data


def cutter_name_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor=connections["default"].cursor()
    sql_cutter = f"""
        select e.emp_paycode as id,e.emp_name as name,t.des_name from {db_name}.dbo.tbemp (nolock) e join {db_name}.dbo.tbdes (nolock) t on e.des_code = t.des_code where e.resign=0
        and e.loc_code ='1' and e.des_code ='50'
    """
    cursor.execute(sql_cutter)
    list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return list

def supervisor_name_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor=connections["default"].cursor()
    sql_cutter = f"""
        select e.emp_paycode as id,e.emp_name as name,t.des_name from {db_name}.dbo.tbemp (nolock) e join {db_name}.dbo.tbdes (nolock) t on e.des_code = t.des_code where e.resign=0
        and e.loc_code ='1' and t.des_name like '%super%' 
    """
    cursor.execute(sql_cutter)
    list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return list

def tailor_name_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor=connections["default"].cursor()
    sql_cutter = f"""
        select e.emp_paycode as id,e.emp_name as name,t.des_name from {db_name}.dbo.tbemp (nolock) e join {db_name}.dbo.tbdes (nolock) t on e.des_code = t.des_code where e.resign=0
        and e.loc_code ='1' and e.des_code ='14'
    """
    cursor.execute(sql_cutter)
    list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return list

def checker_name_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor=connections["default"].cursor()
    sql_cutter = f"""
        select e.emp_paycode as id,e.emp_name as name,t.des_name from {db_name}.dbo.tbemp (nolock) e join {db_name}.dbo.tbdes (nolock) t on e.des_code = t.des_code where e.resign=0
        and e.loc_code ='1' and e.des_code in ('6','74')
    """
    cursor.execute(sql_cutter)
    list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return list

def qa_name_list():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    db_name = pay_db(curr_date)
    cursor=connections["default"].cursor()
    sql_cutter = f"""
        select e.emp_paycode as id,e.emp_name as name,t.des_name from {db_name}.dbo.tbemp (nolock) e join {db_name}.dbo.tbdes (nolock) t on e.des_code = t.des_code where e.resign=0
        and e.loc_code ='1' and e.des_code ='74'
    """
    cursor.execute(sql_cutter)
    list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    return list

def get_trans_srno_data(trans_id,type):
    if trans_id and type:
        cursor = connections['default'].cursor()
        sql = f""" 
            EXEC GET_TRANSACTION_DATA '{trans_id}','{type}'
        """
        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 


def get_trans_srno_data_disp(trans_id,type):
    if trans_id and type:
        cursor = connections['default'].cursor()
        if type == 'stitch':
            sql = f""" 
                select s.trans_id,s.size,s.color,(CASE WHEN s.defect !='None' THEN s.defect ELSE '' END) defect,s.defect_count,s.result,s.created_at,u.full_name as created_by,s.updated_by  
                from stitch_entry_size_dt s
                left join (select id,username,full_name from {intellisync_db}.dbo.user_master) u on u.id  = s.created_by
                where s.trans_id ='{trans_id}'
            """
        elif type == 'finish':
            sql = f""" 
                select s.trans_id,s.size,s.color,(CASE WHEN s.defect !='None' THEN s.defect ELSE '' END) defect,s.defect_count,s.result,s.created_at,u.full_name as created_by,s.updated_by    
                from finish_entry_size_dt s 
                left join (select id,username,full_name from {intellisync_db}.dbo.user_master) u on u.id  = s.created_by
                where s.trans_id ='{trans_id}'
            """
        elif type == 'dispatch':
            sql = f""" 
                select s.trans_id,s.size,s.color,(CASE WHEN s.defect !='None' THEN s.defect ELSE '' END) defect,s.defect_count,s.result,s.created_at,u.full_name as created_by,s.updated_by    
                from dispatch_entry_size_dt s 
                left join (select id,username,full_name from {intellisync_db}.dbo.user_master) u on u.id  = s.created_by
                where s.trans_id ='{trans_id}'
            """

        cursor.execute(sql)
        data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        return data
    return [] 

def sampling_mail_data():
    today_date = datetime.today().strftime('%Y-%m-%d')
    sql_size = f"""
    select c.name as sample_group,booking_no,mh.name as Merchant_head,m.name as Merchant_name, 
    (CASE WHEN booking_type ='F' THEN 'Fresh' WHEN booking_type ='A' THEN 'Alter' WHEN booking_type ='R' THEN 'Resubmission' END) booking_type,buyer_name,style_no,
    st.name as sample_type, p.name as product_type,se.name as season,sey.name as season_year,total_qty,
    CONVERT(varchar, booking_date, 3) booking_date, CONVERT(varchar, target_date, 3) target_date 
    from sample_booking_mt s
    join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) c on c.id =  s.sample_group_type_id
    join (select id,name from {intellisync_db}.dbo.first_level_master group by id,name) st on st.id = s.sample_type_id
    join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) p on p.id =  s.product_type_id
    join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) mh on mh.id =  s.merchant_head_id
    join (select id,name from {intellisync_db}.dbo.first_level_master group by id,name) m on m.id = s.merchant_name_id
    join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) se on se.id =  s.season_id
    join (select id,name from {intellisync_db}.dbo.first_level_master group by id,name) sey on sey.id = s.season_year_id
    where CONVERT(varchar, booking_date, 23) = '{today_date}'
    order by c.name,booking_type,m.name,s.booking_no asc
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data

def sys_para_val(arg):

    sql_size = f"""
    select CONDIDTION as email_list from is_app_db_new.dbo.SystemParameters where ParameterName = '{arg}'
    """
    cursor=connections["default"].cursor()
    cursor.execute(sql_size)
    sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
    cursor.close()
    return sq_data
