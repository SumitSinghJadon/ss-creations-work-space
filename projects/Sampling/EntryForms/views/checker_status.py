from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster
from Sampling_db.models import CheckerStatusMt
from django.contrib import messages

class CheckerStatusView(View):
    def get(self, request):

        checker_status_list   = CommonMaster.objects.filter(type__code='CM22', is_active=True)
        hold_reason_list      = CommonMaster.objects.filter(type__code='CM22', is_active=True)
        delay_reason_list     = CommonMaster.objects.filter(type__code='CM22', is_active=True)

        context = {

            "checker_status_list"   :   checker_status_list,
            "hold_reason_list"      :   hold_reason_list,
            "delay_reason_list"     :   delay_reason_list,
        }
        return render(request, 'checker_status.html', context)
    
    def post(self, request):

        checker_status    = request.POST.get('checker_status')
        deliver_loss_time = request.POST.get('deliver_loss_time')
        remarks           = request.POST.get('remarks')
        returned_date     = request.POST.get('returned_date')
        hold_reason       = request.POST.get('hold_reason')
        delay_reason      = request.POST.get('delay_reason')
        qa_remarks        = request.POST.get('qa_remarks')

        CheckerStatusMt.objects.create(
            checker_status    =  checker_status,  
            deliver_loss_time =  deliver_loss_time,
            remarks           =  remarks,
            returned_date     =  returned_date,
            hold_reason       =  hold_reason,
            delay_reason      =  delay_reason,
            qa_remarks        =  qa_remarks,
        )
        messages.success(request, "Success! The entry has been created.")
        return redirect ('checker_status_page')