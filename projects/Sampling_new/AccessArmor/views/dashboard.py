from django.views import View
from django.shortcuts import redirect, render
# from IntelliSync_db.models import CommonMaster
from django.db import connections, connection
from datetime import datetime , timedelta

import IS_Nexus

class Dashboard(View):
    def get(self, request):
        month = int(datetime.today().strftime('%m'))
        year = int(datetime.today().strftime('%Y'))
        curr_date = datetime.today().strftime('%Y-%m-%d')
        curr_year = int(datetime.today().strftime('%Y'))

        cursor = connections['default'].cursor()
        sql = f"""  EXEC GET_TAILOR_EFF '{month}','{year}','1',8,'total_summ','{curr_date}' """
        cursor.execute(sql)
        tailor_eff_total =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()

        cursor = connections['default'].cursor()
        sql = f"""  EXEC GET_SAMP_DASH 'sample_booking' """
        cursor.execute(sql)
        sample_booking_total =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()

        cursor = connections['default'].cursor()
        sql = f"""  EXEC GET_SAMP_DASH 'pending_booking_confirm' """
        cursor.execute(sql)
        pending_booking_confirm =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()

        # print(tailor_eff_total)
        context = {
            'month' : month,
            'year' : year,
            'tailor_eff_total' : tailor_eff_total,
            'sample_booking_total' : sample_booking_total,
            'pending_booking_confirm' : pending_booking_confirm
        }
        return render(request, 'dashboard.html', context )

