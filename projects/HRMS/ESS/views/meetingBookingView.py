from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from datetime import datetime
from HRMS_db.models import MeetingRoomMaster,MeetingRoomBooking
from IS_Nexus.functions import messages
from IS_Nexus.functions.data_conversion import queryset_to_json
from IS_Nexus.functions.shortcuts import formate_date
from django.core.serializers import serialize

class MeetingBookingView(View):
    def get(self,request):
        location = request.user.location

        if id := request.GET.get('id'):
            data = MeetingRoomBooking.objects.filter(room_name=id)
            room_data = MeetingRoomMaster.objects.get(pk=id)
            context = {
                "meeting_data": data,
                "room_data" : room_data
            }
            return render(request, "eventCalendar.html", context)
        
        elif 'meeting_date' in request.GET and 'start_time' in request.GET and 'end_time' in request.GET:
            meeting_date = request.GET['meeting_date']
            start_time = request.GET['start_time']
            end_time = request.GET['end_time']
            is_available = self.checkTimeslot(meeting_date,start_time,end_time)
            return JsonResponse({'available': is_available})
        
        else:
            data = MeetingRoomMaster.objects.using('default').all()
            context = {
                "meeting_data": data
            }
            return render(request, "meetingBooking.html", context)


    def post(self,request):
        url = self.request.path
        params = self.request.GET

        if params:
            url += '?' + params.urlencode()

        user=request.user
        mr_id = request.POST.get('room_id')
        meeting_room = MeetingRoomMaster.objects.get(pk=mr_id)
        meeting_date = request.POST.get('meeting_date')
        meeting_type = request.POST.get('meeting_type')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose')
        guest_name = request.POST.get('guest_name')
        no_of_attendees = request.POST.get('no_of_attendees')
        buyer = request.POST.get('buyer')
        description = request.POST.get('description')
        booked_on = datetime.now()
        booked_by = request.user.username
        location = request.user.location
        
        mrb = MeetingRoomBooking.objects.create(
            meeting_date = meeting_date,
            meeting_type = meeting_type,
            start_time = start_time,
            end_time = end_time,
            purpose = purpose,
            room_name = meeting_room,
            guest_name = guest_name,
            no_of_attendees = no_of_attendees,
            buyer = buyer,
            location = location,
            description = description,
            user = user
        )
        messages.saved(request)
        return redirect(url)
    
    def checkTimeslot(self,meeting_date,start_time,end_time):
        existing_bookings = MeetingRoomBooking.objects.filter(meeting_date=meeting_date)
        for booking in existing_bookings:
            if booking.start_time <= start_time < booking.end_time:
                return False
            if booking.start_time < end_time <= booking.end_time:
                return False
            if start_time <= booking.start_time and end_time >= booking.end_time:
                return False
        return True