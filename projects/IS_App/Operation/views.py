from django.shortcuts import render
from django.db import connections
from django.core.paginator import Paginator
from rest_framework import viewsets
from django.views import View
from .serializers import FileHandOverSerializer
from App_db.models.file_handover_mt import FileHandOver
import json

from  django.http import JsonResponse

# Create your views here.



class FileHandOverView(View):
    def get(self, request):
            sql_query = """
          SELECT 
			    DISTINCT
				pt.Party_name AS buyer_name,
                t1.buyer,
                t2.styleno,
                t2.Ourref,
                t2.color AS "garment_color",
                t1.orderdate,
                t3.ExDelvDate AS delvdate,
                SUM(t2.totalqty) AS totalqty,
                fhm.pcd_status,
                fhm.reason_notmeet,
                fhm.remark,
                fhm.plan_qty,
                fhm.handover_date,
                fhm.ppc_comment,
                fhm.delivery_status,
                fhm.risk_category,
                fhm.ppm_date,
                fhm.rnd_comp_date,
                fhm.factory_comment,
                fhm.unit_id,
                fhm.id As handover_id
            FROM 
                ExpoHead t1
            JOIN 
                ExpoLotDet t2 ON t1.Ourref = t2.Ourref
            JOIN 
                ExpoLot t3 ON t2.Ourref = t3.Ourref
			JOIN
			    party pt ON t1.buyer = pt.Party_code
            LEFT JOIN 
            is_app_db_new.dbo.file_handover_mt fhm ON t2.Ourref = fhm.ourr_ef

            WHERE 
                t2.Ourref IS NOT NULL AND t2.Ourref <> ''
                AND t1.orderdate > '2024-01-01' 
                AND t1.closed IN ('P','U') 
        GROUP BY
                pt.Party_name,
                t1.buyer,
                t2.styleno,
                t2.Ourref,
                t2.color,
                t1.orderdate,
                t3.ExDelvDate,
                fhm.pcd_status,
                fhm.reason_notmeet,
                fhm.remark,
                fhm.plan_qty,
                fhm.handover_date,
                fhm.ppc_comment,
                fhm.delivery_status,
                fhm.risk_category,
                fhm.ppm_date,
                fhm.rnd_comp_date,
                fhm.factory_comment,
                fhm.unit_id,
                fhm.id;
            """
            
            with connections['erp_db'].cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] 
            
            formatted_rows = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                # Format date fields
                if 'orderdate' in row_dict and row_dict['orderdate']:
                    row_dict['orderdate'] = row_dict['orderdate'].strftime('%Y-%m-%d')
                if 'delvdate' in row_dict and row_dict['delvdate']:
                    row_dict['delvdate'] = row_dict['delvdate'].strftime('%Y-%m-%d')
                if 'handover_date' in row_dict and row_dict['handover_date']:
                        row_dict['handover_date'] = row_dict['handover_date'].strftime('%Y-%m-%d')
                if 'ppm_date' in row_dict and row_dict['ppm_date']:
                        row_dict['ppm_date'] = row_dict['ppm_date'].strftime('%Y-%m-%d')
                if 'rnd_comp_date' in row_dict and row_dict['rnd_comp_date']:
                        row_dict['rnd_comp_date'] = row_dict['rnd_comp_date'].strftime('%Y-%m-%d')
                formatted_rows.append(row_dict)
            
            sql_query2 = """ 
                             SELECT
                               id AS UnitID,
                               name AS Unit
                               FROM location_master
                            """
            
            with connections['intellisync_db'].cursor() as cursor:
                cursor.execute(sql_query2)
                Units = cursor.fetchall()
                
            unit_data = [{'id': unit[0], 'name': unit[1]} for unit in Units]
                

            return JsonResponse({
                                  'data': formatted_rows,
                                  'Units': unit_data},
                                   safe=False)





class FileHandOverViewSet(viewsets.ModelViewSet):
    queryset = FileHandOver.objects.using('is_app').all()
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return FileHandOverSerializer
        elif self.request.method == 'POST':
            return FileHandOverSerializer
    

    quserializer_class = FileHandOverSerializer



class BuyerFilterView(View):
        def get(self, request):
                sql_query = """
           SELECT
                 party_code as buyer_code,
                 party_name as buyer_name 
            from
                 Party p join ExpoHead ex  on ex.buyer = p.party_code
            where  
            ex.closed in ('P','U') and (isbuyer ='1' or isTradingBuyer='1')
            AND ex.orderdate > '2024-01-01'
            group by p.party_code,p.party_name 
            order by p.party_name asc                
                        """
        
                with connections['erp_db'].cursor() as cursor:
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    formatted_rows = [dict(zip(columns, row)) for row in rows]

                return JsonResponse({'filterdata': formatted_rows}, safe=False)
            

class StyleFilterView(View):
        def get(self, request):
                buyer_code = request.GET.get('buyer_code')
                sql_query = """
                    select
                            ed.ourref,
                            ed.styleno from ExpoLotDet ed join ExpoHead ex  on ed.ourref = ex.ourref
                    where 
                            ex.buyer = %s and closed in ('P','U')
                            AND ex.orderdate > '2024-01-01'
                            group by ed.ourref,
                            ed.styleno order by ed.styleno asc
                            
                            """

                with connections['erp_db'].cursor() as cursor:
                    cursor.execute(sql_query, [buyer_code])
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    formatted_rows = [dict(zip(columns, row)) for row in rows]
               
                    
                return JsonResponse({'filterdata': formatted_rows}, safe=False)
            
     

 
        
