from django.views import View
from django.shortcuts import render, redirect
from Sampling_db.models import SampleBookingMt, SampleArticleDetails
from django.db.models import aggregates
from django.contrib import messages
from datetime import datetime, date
from django.utils import timezone
from django.http import HttpResponse
from IS_Nexus.functions.shortcuts import formate_date


class ConcatAgg(aggregates.Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '')"
    allow_distinct = True


class BookingConfirmationView(View):
    def get(self, request):
        bid = request.GET.get("bid")
        mt_data = SampleBookingMt.objects.get(id=bid)
        dt_data = SampleArticleDetails.objects.filter(booking_id=mt_data)
        
        context = {
            'mt_data' : mt_data,
            'dt_data' : dt_data 
        }

        return render(request, 'booking_confirmation.html', context)


    def post(self,request):
        bid = request.GET.get("bid")
        save_flag = False
        booking_mt = SampleBookingMt.objects.get(id = bid)

        if booking_mt:
            try:
                # MT Data
                file_status = request.POST.get('file_status')
                file_rcv_date = request.POST.get('file_rcv_date')
                booking_status = request.POST.get('booking_status')
                booking_hold_reason = request.POST.get('booking_hold_reason')
                booking_cancelled_reason = request.POST.get('booking_cancelled_reason')
                article_status = request.POST.get('article_status')
                article_hold_reason = request.POST.get('article_hold_reason')
                article_reject_reason = request.POST.get('article_reject_reason')
                remarks = request.POST.get('remarks')
                
                
                # Update MT Data
                try:
                    if file_status: booking_mt.file_status = file_status
                    if file_rcv_date: booking_mt.file_rcv_date = formate_date(file_rcv_date)
                    if booking_status: booking_mt.booking_status = booking_status
                    if booking_hold_reason: booking_mt.booking_hold_reason = booking_hold_reason
                    if booking_cancelled_reason: booking_mt.booking_cancelled_reason = booking_cancelled_reason
                    if article_status: booking_mt.material_status = article_status
                    if article_hold_reason: booking_mt.article_hold_reason = article_hold_reason
                    if article_reject_reason: booking_mt.article_reject_reason = article_reject_reason
                    if remarks: booking_mt.remarks = remarks
                    booking_mt.save()
                    save_flag = True

                    # DT data
                    article_counter = request.POST.get('article_counter', 0)

                    try:
                        for i in range(1, int(article_counter)):
                            article_id     = request.POST.get(f'article_id_{i}')
                            received_by_ic = request.POST.get(f'received_by_ic_{i}')
                            received_date  = request.POST.get(f'received_date_{i}')
                            received_date  = formate_date(received_date)

                            booking_dt = SampleArticleDetails.objects.get(id=article_id)
                            booking_dt.confirm_by_inchanrge = received_by_ic
                            booking_dt.received_date = received_date
                            booking_dt.save()
                            save_flag = True

                    except Exception as e:
                        save_flag = False
                        print(e)
                        messages.error(request, "Something Went wrong...")

                except Exception as e:
                    print(e)
                    messages.error(request, "Something Went wrong...")

            except Exception as e:
                print(e)
                messages.error(request, "Something Went wrong...")
        else:
            messages.error(request, 'Related Data not found.')

        if save_flag:
            messages.success(request, 'Data Updated...')


        # counter = request.POST.get('counter')
        # is_saved = ''
        
        # if counter:
        #     counter = int(counter) + 1
        #     for i in range(counter):
        #         booking_id = request.POST.get(f"booking_id[{i}]")
        #         booking_status = request.POST.get(f"booking_status[{i}]","pending")
        #         file_status = request.POST.get(f"file_status[{i}]")
        #         file_rcv_date = request.POST.get(f"file_rcv_date[{i}]")
        #         hold_reason = request.POST.get(f"hold_reason[{i}]")
        #         cancelled_reason = request.POST.get(f"cancelled_reason[{i}]")
        #         remarks = request.POST.get(f"remarks[{i}]")
        #         article_status = request.POST.get(f"article_status[{i}]")

        #         # print(booking_status)
        #         if booking_id and article_status and file_status and file_rcv_date:
        #             file_rcv_date =  datetime.strptime(file_rcv_date, '%Y-%m-%dT%H:%M')

        #             try:
        #                 sample_booking_id = SampleBookingMt.objects.filter(id=booking_id).update(
        #                     material_status = article_status,
        #                     booking_status = booking_status,
        #                     file_status = file_status,
        #                     file_rcv_date = file_rcv_date,
        #                     hold_reason = hold_reason,
        #                     cancelled_reason = cancelled_reason
        #                 )

        #                 is_saved = True

        #             except Exception as e:
        #                 print(e)
        #                 is_saved = False
            
        #     if is_saved:
        #         messages.success(request,'Data saved Success') 
        #     else:
        #         messages.error(request,"Booking Confirmation Failed") 

        return redirect('booking_confirmation_dashboard_page')
        




class BookingConfirmationDashboardView(View):
    def get(self, request):
        from_date = request.GET.get("from_date")
        till_date = request.GET.get("till_date")
        status = request.GET.get("status")

        today = date.today()
        # first_day_of_month = today.replace(day=1)
        # current_mont = first_day_of_month.strftime('%Y-%m-%d')

        mt_data = SampleBookingMt.objects.all().order_by("-booking_date")

        if status:
            mt_data = mt_data.filter(booking_status=status)
        
        if from_date:
            from_datetime = datetime.strptime(from_date, '%Y-%m-%d')
            from_datetime = timezone.make_aware(from_datetime, timezone.get_current_timezone())
            mt_data = mt_data.filter(booking_date__gte=from_datetime)

        if till_date:
            till_datetime = datetime.strptime(till_date, '%Y-%m-%d')
            till_datetime = till_datetime.replace(hour=23, minute=59, second=59)
            till_datetime = timezone.make_aware(till_datetime, timezone.get_current_timezone())
            mt_data = mt_data.filter(booking_date__lte= till_datetime)

        if not(status, from_date, till_date):
            mt_data = mt_data.filter(booking_status='pending')
        
        if not from_date or not till_date:
            pass 

        context = {
            'mt_data' : mt_data,
            'today' : today
        }

        return render(request, 'booking_confirmation_dashboard.html', context)

