from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster, get_next_number
from Sampling_db.models import SampleBookingMt,SampleArticleDetails,SampleSizeQuantity
from django.contrib import messages as msg
from django.http import JsonResponse
from IS_Nexus.database.sampling import get_merchant_by_merchant_head, get_style_by_buyer, get_season_year_by_season
from ERP_db.models import Party, Sizetype, Color
from IS_Nexus.functions import queryset_to_json
from django.db.models import Q
from django.conf import settings
from IS_Nexus.functions.shortcuts import formate_date


class SampleBookingView(View):
    def get(self, request):
        # Send Ajax Data 
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']

        flag = request.GET.get('flag')

        if flag == 'get_merchant_by_merchant_head':
            mid = request.GET.get('merchant_head')
            data = get_merchant_by_merchant_head(mid, fields=['name', 'value', 'id'])
            return JsonResponse(data, safe=False)
        
        elif flag == 'get_style_by_buyer':
            bid = request.GET.get('bid')
            data = get_style_by_buyer(bid, fields=['styleno'])
            return JsonResponse(data, safe=False)
        
        elif flag == 'get_season_year_by_season':
            sid = request.GET.get("sid")
            data = get_season_year_by_season(sid, fields=['name', 'id'])
            return JsonResponse(data, safe=False)

        elif flag == 'get_sample_type_by_sample_group':
            group_id = request.GET.get("sgt_id")
            data = FirstLevelMaster.objects.filter(master_type__code='CT-6', common_master=group_id, is_active=True).values('id', 'name').using('intellisync_db')
            data = queryset_to_json(data)
            return JsonResponse(data, safe=False)
        
        elif flag == 'cancel_booking':
            bid = request.GET.get("bid")
            SampleBookingMt.objects.filter(id=bid).update(
                booking_status = 'cancelled'
            )
            return redirect ('sample_booking_page')


        bid = request.GET.get('bid')
        mt_data = dt_data = None
        sq_data = ['1']

        if bid:
            mt_data = SampleBookingMt.objects.get(id=bid)
            dt_data = SampleArticleDetails.objects.filter(booking_id=mt_data.id)
            sq_data = SampleSizeQuantity.objects.filter(booking_id=mt_data)

        merchant_head_list = CommonMaster.objects.filter(master_type__code='CT-22', is_active=True).using('intellisync_db')
        booking_no_list    = SampleBookingMt.objects.filter(is_active=True).values('id', 'booking_no').order_by("-created_at")
        buyer_list         = Party.objects.filter(active=1, isbuyer=1).values('party_code','party_name','pname').using('erp_db')
        sample_group_list  = CommonMaster.objects.filter(master_type__code='CT-4', is_active=True).using('intellisync_db')
        season_list        = CommonMaster.objects.filter(master_type__code='CT-12', is_active=True).using('intellisync_db')
        product_type_list  = CommonMaster.objects.filter(master_type__code='CT-7', is_active=True).using('intellisync_db')
        article_list       = dt_data or FirstLevelMaster.objects.filter(master_type__code='CT-11', is_active=True).order_by('common_master__value', 'value').using('intellisync_db')
        size_list          = Sizetype.objects.all().values('sizetypeid', 'sizetype')
        color_list         = Color.objects.filter(active=1).values_list('color', flat=True).distinct().exclude(
                                Q(color__contains='0') | Q(color__contains='1') | Q(color__contains='2') | Q(color__contains='3') | 
                                Q(color__contains='4') | Q(color__contains='5') | Q(color__contains='6') | Q(color__contains='7') | 
                                Q(color__contains='8') | Q(color__contains='9') | Q(color__contains='.')
                            )

        context = {
            "booking_no_list"    : booking_no_list,
            "merchant_head_list" : merchant_head_list,
            "buyer_list"         : buyer_list,
            "sample_group_list"  : sample_group_list,
            "season_list"        : season_list,
            "product_type_list"  : product_type_list,
            "article_list"       : article_list,
                 
            "mt_data"            : mt_data,
            "dt_data"            : dt_data,
            "sq_data"            : sq_data,
            "size_list"          : size_list,
            "color_list"         : color_list,
        }

        return render(request, 'sample_booking.html', context)


    def post(self, request):
        # Generate Booking Number
        flag = request.POST.get('flag')
        bid = request.GET.get('bid')

        if not bid:
            booking_no = get_next_number('SMPL')
        else:
            booking_no = SampleBookingMt.objects.get(id=bid).booking_no

        if booking_no:
            # Fetch Data from post request for Sample Booking Mt 
            image1            = request.FILES.get('garment_img_1')
            image2            = request.FILES.get('garment_img_2')
            booking_type      = request.POST.get('booking_type')
            merchant_head     = request.POST.get('merchant_head')
            merchant          = request.POST.get('merchant')
            buyer             = request.POST.get('buyer')
            sample_group_type = request.POST.get('sample_group_type')
            sample_type       = request.POST.get('sample_type')
            style_no          = request.POST.get('style_no')
            season            = request.POST.get('season')
            season_year       = request.POST.get('season_year')
            booking_date      = request.POST.get('booking_date')
            target_date       = request.POST.get('target_date')
            product_type      = request.POST.get('product_type')
            remarks           = request.POST.get('remarks')
            total_qty         = request.POST.get('total_qty')
            reason            = request.POST.get('reason')

            # Verify Data for Related Fields For Sample Booking Mt
            merchant_head     = CommonMaster.objects.using('intellisync_db').get(id=merchant_head, master_type__code='CT-22', is_active=True)
            merchant_name     = FirstLevelMaster.objects.using('intellisync_db').get(id=merchant, master_type__code='CT-23', is_active=True)
            buyer             = Party.objects.using('erp_db').get(active=1, isbuyer=1, party_code=buyer)
            sample_group_type = CommonMaster.objects.using('intellisync_db').get(id=sample_group_type, master_type__code='CT-4', is_active=True)
            # sample_group_type_p = CommonMaster.objects.using('intellisync_db').filter(id=sample_group_type, master_type__code='CT-4', value='P', is_active=True).first()
            sample_type       = FirstLevelMaster.objects.using('intellisync_db').get(id=sample_type, master_type__code='CT-6', is_active=True)
            season            = CommonMaster.objects.get(id=season, is_active=True)
            season_year       = FirstLevelMaster.objects.get(id=season_year, is_active=True)
            product_type      = CommonMaster.objects.get(id=product_type, is_active=True)
            booking_date      = formate_date(booking_date)
            target_date       = formate_date(target_date)

            # Save Data in Sample Booking MT
            create_data = {
                "booking_no"        : booking_no,
                "booking_type"      : booking_type,
                "merchant_head"     : merchant_head,
                "merchant_name"     : merchant_name,
                "buyer_code"        : buyer.party_code,
                "buyer_name"        : buyer.party_name,
                "sample_group_type" : sample_group_type,
                "sample_type"       : sample_type,
                "style_no"          : style_no,
                "season"            : season,
                "season_year"       : season_year,
                "booking_date"      : booking_date,
                "target_date"       : target_date,
                "product_type"      : product_type,
                "remarks"           : remarks,
                "total_qty"         : total_qty,
                "reason"            : reason,
                "created_by"        : request.user
            }

            # Save Images
            if image1: create_data['image1'] = image1
            if image2: create_data['image2'] = image2

            # Check If Booking is already created with same data
            sample_data = SampleBookingMt.objects.filter(
                buyer_code = buyer.party_code, 
                style_no = style_no, 
                season = season, 
                season_year = season_year,
                sample_type = sample_type,
            ).first()

            if sample_data and not bid and sample_data.sample_group_type.value == 'P':
                # Show error new entry already exist in database 
                msg.error(request, 'This booking is already booked (Buyer, Style, Season, Sample Type)')
            
            else:
                if bid:
                    # Update Booking
                    booking_id = SampleBookingMt.objects.get(id=bid)
                    del create_data['created_by']
                    for key, value in create_data.items():
                        setattr(booking_id, key, value)
                    booking_id.save()

                else:
                    # Create New Booking
                    # create_data["created_by"] = request.user,
                    booking_id = SampleBookingMt.objects.create(**create_data)
                
                if booking_id:
                    # Fetch Data for Sample Article Details
                    article_counter = request.POST.get('article_counter')
                    SAD_obj_list = []

                    for i in range(1, int(article_counter)+1):
                        given_by_merchant = request.POST.get(f'given_by_merchant_{i}')
                        article           = request.POST.get(f'article_{i}', None)
                        comment           = request.POST.get(f'comment_{i}', None)
                        details           = request.POST.get(f'details_{i}', None)
                        expected_date_str = request.POST.get(f'expected_date_{i}')
                        expected_date     = formate_date(expected_date_str)

                        # Verify article name
                        article = FirstLevelMaster.objects.using('intellisync_db').get(master_type__code='CT-11', id=article, is_active=True)

                        if given_by_merchant and article:
                            sad_obj = SampleArticleDetails(
                                booking_id        = booking_id,
                                booking_no        = booking_no,
                                given_by_merchant = given_by_merchant,
                                article           = article,
                                comment           = comment,
                                details           = details,
                                expected_date     = expected_date 
                            )

                            SAD_obj_list.append(sad_obj)
                    
                    SampleArticleDetails.objects.filter(booking_no = booking_no).delete()
                    SampleArticleDetails.objects.bulk_create(SAD_obj_list)

                    # Fetch Date for SampleSizeQuantity
                    size_list     = request.POST.getlist('size')
                    color_list    = request.POST.getlist('color')
                    quantity_list = request.POST.getlist('quantity')
                    total_qty     = 0 

                    SSQ_list = []
                    for size, color, quantity in zip(size_list, color_list, quantity_list):
                        if size and color:
                            total_qty = total_qty + int(quantity)
                            ssq_obj = SampleSizeQuantity(
                                booking_id = booking_id,
                                booking_no = booking_no,
                                size       = str(size).upper(),
                                color      = color,
                                quantity   = quantity,
                            )
                            SSQ_list.append(ssq_obj)

                    booking_id.total_qty = total_qty
                    SampleSizeQuantity.objects.filter(booking_no = booking_no).delete()
                    SampleSizeQuantity.objects.bulk_create(SSQ_list)
                    booking_id.save()

            #         except Exception as e:
            #             print(e)
            #             SampleSizeQuantity.objects.filter(booking_id=booking_id).delete()
            #             booking_id.delete()
            #             msg.error(request, 'Unable to save Size wise Quantity')

            #     except Exception as e:
            #         print(e)
            #         booking_id.delete() 
            #         msg.error(request, 'Unable to save Size wise Quantity')
            
            # except Exception as e:
            #     print(e)
            #     msg.error(request, 'Unable to save Size wise Quantity')
            #     messages.form_error(request)

        else:
            msg.error(request, 'Unable to generate booking number.')

        return redirect ('sample_booking_page')
