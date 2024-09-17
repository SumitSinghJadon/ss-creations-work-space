from django.views import View
from django.shortcuts import render
from .sample_booking import SampleBookingMt, SampleArticleDetails, SampleSizeQuantity
from ERP_db.models import Party


class SamplePrintView(View):
    def get(self, request):
        bid = request.GET.get('bid')

        try:
            mt_data = SampleBookingMt.objects.get(id=bid)
            dt_data = SampleArticleDetails.objects.filter(booking_id=mt_data, given_by_merchant__in=['pa', 'no', 'yes'])
            sq_data = SampleSizeQuantity.objects.filter(booking_id=mt_data)

            context ={
                "mt_data" : mt_data,
                "dt_data" : dt_data,
                "sq_data" : sq_data,
            }
            
        except Exception as e:
            print(e)
            sample_data = None
            context = {}

        
        return render(request, 'sample_print.html',context)

