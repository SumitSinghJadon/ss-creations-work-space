
from django.db import connections
from django.views import View
from  django.http import JsonResponse

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
            order by p.party_name asc                
                        """
                with connections['erp_db'].cursor() as cursor:
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    formatted_rows = [dict(zip(columns, row)) for row in rows]
                print(formatted_rows)
                    
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
                print("formate",formatted_rows)    
                return JsonResponse({'filterdata': formatted_rows}, safe=False)
        
        


class OurRefFilterView(View):
    def get(self, request):
        styleno = request.GET.get('styleno')
        sql_query = """
            SELECT
                ed.ourref,
                ed.styleno
            FROM
                ExpoLotDet ed
            JOIN
                ExpoHead ex ON ed.ourref = ex.ourref
            WHERE
                ed.styleno = %s
                AND ex.closed IN ('P', 'U')
                AND ex.orderdate > '2024-01-01'
            GROUP BY
                ed.ourref,
                ed.styleno
            ORDER BY
                ed.styleno ASC
        """

        with connections['erp_db'].cursor() as cursor:
            cursor.execute(sql_query, [styleno])
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            formatted_rows = [dict(zip(columns, row)) for row in rows]
        
        print("formatted", formatted_rows)    
        return JsonResponse({'filterdata': formatted_rows}, safe=False)


