from django.views import View
from django.shortcuts import render
from django.db import connections
from datetime import datetime
# from django.http import JsonResponse
# import json

class AirFreightForm(View):
    def get(self, request):
        from_date_str = request.GET.get('from_date')
        till_date_str = request.GET.get('till_date')
        if from_date_str and till_date_str:
            from_date = datetime.strptime(from_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            till_date = datetime.strptime(till_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            sql_query = f""" SELECT  
                i.InvoiceNo,i.dated,i.Mode,i.InvHomeLocation,i.HomeLocation,i.Buyer,d.styleno,p.party_name,i.TotalQty,id.Quantity
                FROM VisualGEMS.dbo.Invoice i
                JOIN VisualGEMS.dbo.Invoicedtl d ON i.invoiceNo = d.invoiceNo
                JOIN VisualGEMS.dbo.Party p ON i.Buyer = p.party_code
                JOIN VisualGEMS.dbo.Invoicedtl id ON i.InvoiceNo = id.InvoiceNo
                WHERE i.dated >= '{from_date}' AND i.dated <= '{till_date}' AND Mode = 'Air'
                ORDER BY i.dated;
                        """
            with connections["default"].cursor() as cursor:
                cursor.execute(sql_query)
                data_list = [{cursor.description[i][0]: value for i,value in enumerate(row)} for row in cursor.fetchall()]
                print('okay',data_list)
            context = {
                'data_list':data_list
            }
            return render(request, 'air_freight_form.html',context)
        return render(request, 'air_freight_form.html')