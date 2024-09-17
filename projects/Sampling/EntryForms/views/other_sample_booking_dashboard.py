from django.views import View
from django.shortcuts import render
from Sampling_db.models import OtherTransMt
from django.utils import timezone
from datetime import datetime
from IntelliSync_db.models import FirstLevelMaster
from django.db.models import Q 
from IntelliSync_db.models import CommonMaster


class OtherSampleBookingDashboard(View):
    def get(self, request):
        buyer = request.GET.get('buyer')
        from_date = request.GET.get('from_date')
        till_date = request.GET.get('till_date')

        buyer_list = OtherTransMt.objects.filter(is_active=True).values('buyer_name', 'buyer_code').order_by('buyer_name').distinct()
        process_type_list       = FirstLevelMaster.objects.filter(common_master_id='157', is_active=True).order_by('name').using('intellisync_db').values('id','name')
        
        if request.user.is_superuser:
            data_list = OtherTransMt.objects.all()

        else:
            merchant_head = CommonMaster.objects.filter(is_active=True, value=request.user.username, master_type__code='CT-22').first()

            data_list = OtherTransMt.objects.filter(is_active=True).filter(
                Q(created_by = request.user) | Q(merchant_head = merchant_head)
            )
        
        # created_by=request.user
        if buyer:
            data_list = data_list.filter(buyer_code = buyer)
        
        if from_date:
            from_datetime = datetime.strptime(from_date, '%Y-%m-%d')
            from_datetime = timezone.make_aware(from_datetime, timezone.get_current_timezone())
            data_list = data_list.filter(booking_date__gte=from_datetime)

        if till_date:
            till_datetime = datetime.strptime(till_date, '%Y-%m-%d')
            till_datetime = till_datetime.replace(hour=23, minute=59, second=59)
            till_datetime = timezone.make_aware(till_datetime, timezone.get_current_timezone())
            data_list = data_list.filter(booking_date__lte=till_datetime)

        context = {
            'data_list' : data_list.order_by("-created_at"),
            'buyer_list' : buyer_list,
            'process_type_list' : process_type_list
        }
        
        return render(request, 'other_sample_booking_dashboard.html', context)
    
