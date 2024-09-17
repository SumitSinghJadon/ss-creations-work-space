from django.views import View
from django.shortcuts import render
from IntelliSync_db.models import CommonMaster, FirstLevelMaster , SecondLevelMaster
from django.contrib import messages
from django.db import connection,connections
from datetime import datetime , timedelta
from functions import (samp_booking_data , trans_stitching_size_color_wise_qty, 
                       trans_finishing_size_color_wise_qty ,
                       trans_cutting_size_color_wise_qty , qa_name_list, tailor_name_list , 
                       trans_sample_size_color_wise_qty , trans_other_size_color_wise_qty
                    )

class TransactionSizeEntryView(View):
    def get(self, request):
        bid = request.GET.get('bid')
        trans_type = request.GET.get('trans_type')
        
        if trans_type == 'finish':
            sq_data = trans_stitching_size_color_wise_qty(bid)
        elif trans_type == 'dispatch':
            sq_data = trans_finishing_size_color_wise_qty(bid)
        elif trans_type == 'stitch':
            sq_data = trans_cutting_size_color_wise_qty(bid)
        elif trans_type == 'cutting':
            sq_data = trans_sample_size_color_wise_qty(bid)
        elif trans_type == 'other':
            sq_data = trans_other_size_color_wise_qty(bid)            
        # for item in defect_list:
        #     print('\n\n', item.master_type.code, '\n\n')
        
        context ={
            'sq_data' : sq_data,
        }
        return render(request, 'transaction_size_entry.html',context)
    

    def post(self, request):
        pass