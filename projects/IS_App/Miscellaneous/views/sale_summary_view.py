from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.db import connections
from datetime import datetime
import json

class SaleSummaryView(View):
    def get_summary_data(self, from_date, till_date, nulls, summaries):
        try:
            with connections['is_app'].cursor() as cursor:
                query = f"EXEC [GET_SALE_TURNOVER] '{from_date}','{till_date}',{nulls},'{summaries}'"
                print('ok',query)
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]
            return results
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
           
    def get(self, request, *args, **kwargs):
        from_date_str = request.GET.get('from_date')
        till_date_str = request.GET.get('till_date')
        nulls = request.GET.get('nulls')
        summaries = request.GET.get('summaries')
        print("received parameters:", from_date_str, till_date_str, nulls, summaries)
        
        if from_date_str and till_date_str:
            from_date = datetime.strptime(from_date_str, "%d-%m-%Y")
            from_date = from_date.strftime("%d-%m-%Y")
            till_date = datetime.strptime(till_date_str, "%d-%m-%Y")
            till_date = till_date.strftime("%d-%m-%Y")
            result = self.get_summary_data(from_date, till_date, nulls, summaries)
            if result is not None:
                print('/n/n/n',result)
                context = {
                    'json_result': result,
                    'from_date_filt' : from_date,
                    'till_date_filt' :till_date,
                    'from_date' : from_date,  
                    'till_date' :till_date,
                }
                return render(request, 'sale_summary.html', context)
        return render(request, 'sale_summary.html')
           