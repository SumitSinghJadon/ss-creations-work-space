from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from IntelliSync_db.models.common_master import FirstLevelMaster
from App_db.models.buyer_claim import BuyerClaimModel
from ERP_db.models.invoice import Invoice
from django.db import connections
from datetime import datetime

class BuyerClaimView(View):
    def get(self, request):
        reason_type = FirstLevelMaster.objects.filter(common_master_id='171')
        claim_type_list = BuyerClaimModel.CLAIM_TYPE
        unique_years = sorted( Invoice.objects.values_list('yr', flat=True).distinct(), key=lambda x: int(x.split('-')[0]),reverse=True)

        flag = request.GET.get('flag')
        mid = request.GET.get('financial_year')
        inv = request.GET.get('invoice_no')

        if flag == 'get_invoice_by_year':
            if mid:
                sql_query = f"""
                    SELECT invoiceno FROM VisualGEMS.dbo.Invoice WHERE Yr = '{mid}';
                """
                with connections["default"].cursor() as cursor:
                    cursor.eecute(sql_query)
                    invoice_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
                return JsonResponse(invoice_list, safe=False)

        
        elif flag == 'get_buyer_style_unit_by_invoice':
            if mid and inv:
                sql_query = f"""
                    SELECT DISTINCT i.FOBValue,i.InvHomeLocation,i.HomeLocation,i.Buyer,i.Currency, d.styleno, p.party_name,p.party_name
                    FROM VisualGEMS.dbo.Invoice i
                    JOIN VisualGEMS.dbo.Invoicedtl d ON i.invoiceNo = d.invoiceNo
                    JOIN VisualGEMS.dbo.Party p ON i.Buyer = p.party_code
                    WHERE i.InvoiceNo = '{inv}' AND i.Yr = '{mid}';
                """
                with connections["default"].cursor() as cursor:
                    cursor.execute(sql_query)
                    buyer_style_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
                return JsonResponse(buyer_style_list, safe=False)
        
        context = {
            'reason_type': reason_type,
            'claim_type_list': claim_type_list,
            'unique_years': unique_years,
        }
        return render(request, 'buyer_claim_entry_form.html', context)
    def post(self,request):
        if request.method == 'POST':
            financial_years = request.POST.get('financial_year')
            claim_types = request.POST.get('type')
            claim_date = request.POST.get('claim_date')
            changed_claim_date = datetime.strptime(claim_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            invoice_number = request.POST.get('invoice_no')
            buyer_codes = request.POST.get('buyer_code')
            style_type = request.POST.get('styles')
            unit_codes = request.POST.get('unit_code')
            amount_fcc = request.POST.get('amount_fc')
            currencies = request.POST.get('currency')
            conversion_rates = request.POST.get('conversion_rate')
            amounts = request.POST.get('amount')
            debit_note_amounts = request.POST.get('debit_note_amount')
            debit_numbers = request.POST.get('debit_no')
            reasons = request.POST.get('reason')
            remarks = request.POST.get('remarks')
            crt = BuyerClaimModel.objects.create(financial_year = financial_years,
                loss_type = claim_types,
                loss_date = changed_claim_date,
                invoice_no = invoice_number,
                buyer = buyer_codes,
                style = style_type,
                unit_name = unit_codes,
                amount_fc = amount_fcc,
                currency = currencies,
                conversion_rate = conversion_rates,
                amount = amounts,
                debit_note_amount = debit_note_amounts,
                debit_no = debit_numbers,
                reason = reasons,
                remarks = remarks,
            )
            if crt:
                msg = 'Claim Registered Successfully'
                return redirect('buyerClaimEntry')
        return render(request,'buyer_claim_entry_form.html')
