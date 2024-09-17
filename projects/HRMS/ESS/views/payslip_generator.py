import calendar
from django.views import View
from datetime import datetime
from django.db import connections
from django.shortcuts import render
from IS_Nexus.functions.shortcuts import pay_db
from IS_Nexus.database.is_hrms import get_payroll_db_name
from IntelliSync_db.models import CommonMaster


class PayslipGenerator(View):

    def get(self,request):
        
        user=request.user.username
        year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name').order_by('-name')
        month_list = CommonMaster.get_month_list()
        
        context={
            "year_list":year_list,
            "month_list":month_list
        }

        if request.GET.get('year') is not None and request.GET.get('month') is not None:
            year=request.GET.get('year')
            month=request.GET.get('month')
            curr_date =f'{year}-0{month}-01' if int(month)<10 else f'{year}-{month}-01'
            
            current_month=calendar.month_abbr[int(month)].upper()
            if int(month) < 4:
                if int(month) == 1 :
                    month = '13'
                elif int(month) == 2 :
                    month = '14'
                elif int(month) == 3 :
                    month = '15'
                    
            db_name = pay_db(curr_date)
            cursor =  connections[get_payroll_db_name(datetime.now())].cursor()      
            query=f"SELECT tbpfmast.pf_name FROM {db_name}.dbo.tbpfmast"
            cursor.execute(query)
            result = cursor.fetchone()
            pf_prefix=""
            if result:
                pf_prefix = result[0].split("/")[0]
            query = f"""
                SELECT tbemp.emp_paycode, tbmonth_hist.earn4, tbmonth_hist.earn3, 
                tbmonth_hist.earn2, tbmonth_hist.earn1, tbmonth_hist.totrate, 
                tbmonth_hist.earnr4, tbmonth_hist.earnr3, tbmonth_hist.earnr2, 
                tbmonth_hist.earnr1, tbmatd.pd, tbmatd.ab, tbmatd.hd, tbmatd.wo, 
                tbmatd.wd, tbmatd.SL, tbmatd.CL, tbmatd.EL, tbemp.emp_cardno, 
                tbemp.emp_doj, tbemp.emp_name, tbemp.emp_fname, tbdes.des_name,
                tbdep.dep_name, tbemp.esi_no, tbemp.bankac_no, tbmonth_hist.ded1, tbmonth_hist.ded6, tbmonth_hist.ded7, tbmonth_hist.totded, 
                tbmonth_hist.earr1, tbmonth_hist.earr2, tbmonth_hist.earr3, tbmonth_hist.earr4, tbmonth_hist.totarr, tbmonth_hist.otamt1, 
                tbmonth_hist.month_no, tbemp.tmp_sal, tbmonth_hist.othrs1, tbmonth_hist.totearn, tbmonth_hist.ded2, tbmonth_hist.netsal, tbmonth_hist.otesi, 
                tbemp.pf_no, tblocation.loc_pfno1 , tblocation.loc_add1 , tbmonth_hist.ded4, tbmonth_hist.ded5, tbmonth_hist.elday, tbmonth_hist.elamt, tbmonth_hist.otrate1, tbemp.ot_alw, 
                tbbank.bank_name, tbemp.pay_mode, tbemp.old_pfno, tbmatd.BEL, tbmatd.BCL, tbmatd.BSL, tbmonth_hist.npamt, tbmonth_hist.dnot_amt, tbmonth_hist.earnr5, 
                tbmonth_hist.earr5, tbmonth_hist.earn5, tbmatd.SP , tbcmp.cmp_name
                FROM   
                (((((tbemp tbemp INNER JOIN tbdep tbdep ON tbemp.dep_code=tbdep.dep_code) 
                INNER JOIN tbdes tbdes ON tbemp.des_code=tbdes.des_code) 
                INNER JOIN tblocation tblocation ON tbemp.loc_code=tblocation.loc_code)
                INNER JOIN {db_name}.dbo.tbcmp tbcmp ON (tbemp.cmp_code=tbcmp.cmp_code)  
                INNER JOIN {db_name}.dbo.tbmatd tbmatd ON tbemp.emp_code=tbmatd.emp_code)
                INNER JOIN {db_name}.dbo.tbbank tbbank ON tbemp.bank_code=tbbank.bank_code) 
                INNER JOIN {db_name}.dbo.tbmonth_hist tbmonth_hist ON (tbmatd.emp_code=tbmonth_hist.emp_code) 
                AND (tbmatd.month_no=tbmonth_hist.month_no)
                WHERE  tbmonth_hist.month_no='{month}' and tbemp.emp_paycode='{user}'
            """
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            result = [dict((col, val.strip()) if isinstance(val, str) else (col, val) for col, val in zip(columns, row)) for row in data]
            
            context["data"]=result
            context["month"]=current_month
            context["pf_prefix"]=pf_prefix

        return render(request,"payslipGenerate.html",context)
        


    
