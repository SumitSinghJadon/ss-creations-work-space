from django.views import View
from django.shortcuts import render
from datetime import datetime, timedelta
from django.db import connections
from ERP_db.models.buss_location import Busslocation

class BuyerClaimDetailView(View):

    def get_buyer_claim_details(self, from_date, till_date, unit_codes):
        print('ab to query')
        query = f"""
        SELECT b.created_at, b.id, b.financial_year, b.loss_type, b.loss_date, b.invoice_no, b.buyer, b.style, 
               b.unit_name, b.amount_fc, b.currency, b.conversion_rate, b.amount, b.debit_note_amount, 
               b.debit_no, b.reason, b.remarks, p.party_name, d.BLocatShortCode 
        FROM is_app_db_new.dbo.buyer_claim b
        JOIN VisualGEMS.dbo.Party p ON b.Buyer = p.party_code
        JOIN VisualGEMS.dbo.BussLocation d ON b.unit_name = d.BussLocatCode
        WHERE loss_date BETWEEN '{from_date}' AND '{till_date}' AND unit_name = '{unit_codes}';
        """
        
        print(f"Executing query: {query}")
        
        with connections['is_app'].cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
            print('Query results:', results)
        
        return results

    def get(self, request, *args, **kwargs):
        from_date_str = request.GET.get('from_date')
        till_date_str = request.GET.get('till_date')
        unit_codes = request.GET.get('unit_code')
        print(f" fd '{from_date_str}',td '{till_date_str}',uc '{unit_codes}' ")

        unit_code_data = Busslocation.objects.values('busslocatcode', 'blocatshortcode')
        print('Unit code data:', list(unit_code_data))
        
        current_date = datetime.now()
        if current_date.month < 4:
            start_of_financial_year = datetime(current_date.year - 1, 4, 1)
        else:
            start_of_financial_year = datetime(current_date.year, 4, 1)
        
        start_of_financial_year_str = start_of_financial_year.strftime('%Y-%m-%d')
        current_date_str = current_date.strftime('%Y-%m-%d')
        
        if from_date_str and till_date_str and unit_codes:
            print('Processing dates and unit codes...')
            from_date = datetime.strptime(from_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            till_date = datetime.strptime(till_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            result = self.get_buyer_claim_details(from_date, till_date, unit_codes)

            if result:
                for item in result:
                    created_at = item['created_at']
                    item['can_edit'] = (current_date - created_at) <= timedelta(hours=24)

                context = {
                    'json_result': result,
                    'current_date': current_date_str,
                    'unit_code_data': unit_code_data,
                    'from_date': from_date,
                    'till_date': till_date,
                    'is_superuser': request.user.is_superuser,
                    'start_of_financial_year': start_of_financial_year_str,
                }
                print('Context with results:', context)
                return render(request, 'buyer_claim_details.html', context)

        context = {
            'unit_code_data': unit_code_data,
            'current_date': current_date_str,
            'start_of_financial_year': start_of_financial_year_str,
        }
        print('Context without results:', context)
        return render(request, 'buyer_claim_details.html', context)
from django.views import View
from django.shortcuts import render
from datetime import datetime, timedelta
from django.db import connections
from ERP_db.models.buss_location import Busslocation

class BuyerClaimDetailView(View):

    def get_buyer_claim_details(self, from_date, till_date, unit_codes):
        print('ab to query')
        query = f"""
            SELECT b.created_at, b.id, b.financial_year, b.loss_type, b.loss_date, b.invoice_no, b.buyer, b.style,
            b.unit_name, b.amount_fc, b.currency, b.conversion_rate, b.amount, b.debit_note_amount,
            b.debit_no, b.reason, b.remarks, p.party_name, d.BLocatShortCode
            FROM is_app_db_new.dbo.buyer_claim b
            JOIN VisualGEMS.dbo.Party p ON b.Buyer = p.party_code
            JOIN VisualGEMS.dbo.BussLocation d ON b.unit_name = d.BussLocatCode
            WHERE loss_date BETWEEN '{from_date}' AND '{till_date}' AND 
            unit_name = isnull(unit_name,'{unit_codes}')
            """        
        with connections['is_app'].cursor() as cursor:
            cursor.execute(query)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return data_list

    def get(self, request, *args, **kwargs):
        from_date_str = request.GET.get('from_date')
        till_date_str = request.GET.get('till_date')
        unit_codes = request.GET.get('unit_code')

        unit_code_data = Busslocation.objects.values('busslocatcode', 'blocatshortcode')
        
        current_date = datetime.now()
        if current_date.month < 4:
            start_of_financial_year = datetime(current_date.year - 1, 4, 1)
        else:
            start_of_financial_year = datetime(current_date.year, 4, 1)
        
        start_of_financial_year_str = start_of_financial_year.strftime('%Y-%m-%d')
        current_date_str = current_date.strftime('%Y-%m-%d')
        
        if from_date_str and till_date_str and unit_codes:
            from_date = datetime.strptime(from_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            till_date = datetime.strptime(till_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            result = self.get_buyer_claim_details(from_date, till_date, unit_codes)

            if result:
                for item in result:
                    created_at = item['created_at']
                    item['can_edit'] = (current_date - created_at) <= timedelta(hours=24)

                context = {
                    'json_result': result,
                    'current_date': current_date_str,
                    'unit_code_data': unit_code_data,
                    'from_date': from_date,
                    'till_date': till_date,
                    'is_superuser': request.user.is_superuser,
                    'start_of_financial_year': start_of_financial_year_str,
                }
                return render(request, 'buyer_claim_details.html', context)

        context = {
            'unit_code_data': unit_code_data,
            'current_date': current_date_str,
            'start_of_financial_year': start_of_financial_year_str,
        }
        return render(request, 'buyer_claim_details.html', context)
