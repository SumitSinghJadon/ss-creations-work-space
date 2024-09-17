# import qrcode
import base64
from io import BytesIO
from django.views import View
from django.shortcuts import render
from IS_Nexus.database.is_hrms import get_payroll_db_name
from datetime import datetime
from django.db import connections
from Payroll_db.models import DepartmentMaster,EmployeeMaster
from IntelliSync_db.models import LocationMaster
from IS_Nexus.functions.shortcuts import pay_db



class GenerateIdCardView(View):
    def get(self,request):
        
        dep_list=DepartmentMaster.objects.using(get_payroll_db_name(datetime.now())).values('dep_code','dep_name')
        loc_list=LocationMaster.objects.values('name','payroll_code')
        context={
            'dep_list':dep_list,
            'loc_list':loc_list
        }
        department=request.GET.get('department')
        unit=request.GET.get('unit')
        if department and unit:
            emp_list=EmployeeMaster.objects.using(get_payroll_db_name(datetime.now())).values('emp_paycode','emp_name','des_code__des_name','dep_code__dep_code','emp_padd')
            context['emp_list']=emp_list
        # emp_paycode=request.GET.get('emp_paycode')
        # if emp_paycode:
        #     db_name = pay_db(datetime.now().strftime('%Y-%m-%d'))
        #     query=f"""SELECT tbemp.emp_paycode, tbemp.emp_cardno, 
        #     tbemp.emp_name, tbemp.emp_padd, tbdes.des_name,
        #     tbdep.dep_name, tbcmp.cmp_name,tbemp.emp_phn,tblocation.loc_add1,
        #     tbcmp.cmp_ph1
        #     FROM   
        #     {db_name}.dbo.tbemp tbemp INNER JOIN {db_name}.dbo.tbdep tbdep ON tbemp.dep_code=tbdep.dep_code
        #     INNER JOIN {db_name}.dbo.tbdes tbdes ON tbemp.des_code=tbdes.des_code
        #     INNER JOIN {db_name}.dbo.tblocation tblocation ON tbemp.loc_code=tblocation.loc_code
        #     INNER JOIN {db_name}.dbo.tbcmp tbcmp ON tbemp.cmp_code=tbcmp.cmp_code 
        #     WHERE  tbemp.emp_paycode='{emp_paycode}'"""
            
        #     cursor =  connections[get_payroll_db_name(datetime.now())].cursor()
        #     cursor.execute(query)
        #     columns = [col[0] for col in cursor.description]
        #     data = cursor.fetchall()
        #     result = [dict((col, val.strip()) if isinstance(val, str) else (col, val) for col, val in zip(columns, row)) for row in data]
        #     context["data"]=result
        #     qr = qrcode.QRCode(
        #         version=1,
        #         error_correction=qrcode.constants.ERROR_CORRECT_L,
        #         box_size=10,
        #         border=0,  # Set border to 0
        #     )
        #     qr.add_data(emp_paycode)
        #     qr.make(fit=True)
        #     qr_img = qr.make_image(fill_color="black", back_color="white")
        #     buffered = BytesIO()
        #     qr_img.save(buffered, format="PNG")
        #     context["qr_code"] = base64.b64encode(buffered.getvalue()).decode()
        
        return render(request,'new/generate_id_card.html',context)
    

        