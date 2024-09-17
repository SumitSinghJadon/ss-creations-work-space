import datetime
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from QMS_db.models import RtqmCounter, RtqmDefectDT, SewingLineInputMt, SewingLineInputDt, QmsPlaning, ObMaster
from QMS_db.models import StyleSilhouettes
from django.db.models import Count

class SewingTvDashboard(View):
    @csrf_exempt
    def get(self, request, format=None):
        line_id = request.GET.get('line_id')
        # line_id = 10222
        current_date = datetime.datetime.now().strftime('%m/%d/%Y') 
        
        plan = RtqmCounter.objects.filter(rtqm_mt__planing__line__id=line_id).last()
        
        plan_data = QmsPlaning.objects.filter(id=plan.rtqm_mt.planing.id).first()
        
        exists_list = SewingLineInputMt.objects.filter(planing__line__id=plan.rtqm_mt.planing.line.id)
        today_input = 0
        for exists in exists_list:
            size_dt_data = SewingLineInputDt.objects.filter(mt_id__id=exists.id, entry_date=current_date)
            today_input += sum(size.input_qty for size in size_dt_data)

        total_input_data = SewingLineInputDt.objects.filter(mt_id__planing__line__id=plan.rtqm_mt.planing.line.id)
        total_input = sum(item.input_qty for item in total_input_data)
        
        obj_counter = RtqmCounter.objects.filter(rtqm_mt__planing__line__id=plan.rtqm_mt.planing.line.id)
        today_output = obj_counter.filter(entry_date=current_date).count()
        total_output = obj_counter.count()
        today_defect = obj_counter.filter(entry_date=current_date, status='DEFECT').count()
        total_defect = obj_counter.filter(status='DEFECT').count()
        today_rectified = obj_counter.filter(entry_date=current_date, rectified='RECTIFIED').count()
        total_rectified = obj_counter.filter(rectified='RECTIFIED').count()
        
        today_rft = obj_counter.filter(entry_date=current_date, status='RFT').count() 
        total_rft = obj_counter.filter(status='RFT').count() 
        today_total_no_def = RtqmDefectDT.objects.filter(rtqm_mt__planing__line__id=plan.rtqm_mt.planing.line.id, entry_date=current_date).count()
        
        obmaster = ObMaster.objects.filter(buyer_code=plan.rtqm_mt.planing.buyer, style=plan.rtqm_mt.planing.styleno).first()
        
        
        
        actual_pass = today_rft + today_rectified
        wip = total_input - total_output
        rft = 0 if today_output == 0 else round(today_rft / today_output * 100, 2)
        dhu = 0 if today_output == 0 else round(today_total_no_def / today_output * 100, 2)
        defective = 0 if today_output == 0 else round((today_defect / today_output) * 100, 2)
        alter_balance = total_defect - total_rectified
        
        if obmaster is not None:
            eff = round(obmaster.line_sam * (today_rft + today_rectified) / 480, 2) #480mint
        else:
            eff = 0  

        formulas = {
            'today_input': today_input,
            'total_input': total_input,
            'total_output': total_output,
            'today_output': today_output,
            'today_defect': today_defect,
            'total_defect': total_defect,
            'today_rft': today_rft,
            'total_rft': total_rft,
            'total_rectified': total_rectified,
            'today_rectified': today_rectified,
            'actual_pass': actual_pass,
            'wip': wip,
            'eff_percentage':eff,
            'rft_percentage': rft,
            'dhu_percentage': dhu,
            'defective_percentage': defective,
            'alter_balance': alter_balance,
            'today_total_no_def': today_total_no_def,
        }
        
        context = {
            'formulas': formulas,
            'plan_data': {
                'id': plan_data.id,
                'buyer': plan_data.buyer_name,
                'style' :plan_data.styleno,
                'color':plan_data.color  ,
                'line': plan_data.line.name
            },
        }
        
        return JsonResponse(context, safe=False)
    





class SewingTvDashboard2(View):
    
    def get(self,request):
        line_id = request.GET.get('line_id')
        silhouettes_data = self.get_silhouettes(line_id)
        return JsonResponse(silhouettes_data,safe=False)

    
    def get_silhouettes(self, line_id):
        current_date = datetime.datetime.now().strftime('%m/%d/%Y')
        plan = RtqmCounter.objects.filter(rtqm_mt__planing__line__id=line_id).last()
        
        if not plan:
            return {"error":"Plan nahi aa raha"}
        
        plan_data = QmsPlaning.objects.filter(id=plan.rtqm_mt.planing.id).first()

        if not plan_data:
            return None

        silhouettes_data = StyleSilhouettes.objects.filter(
            buyer=plan_data.buyer,
            style_no=plan_data.styleno
        ).first()

        if not silhouettes_data:
            return None
        today_total_defect = RtqmDefectDT.objects.filter(
            rtqm_mt__planing__line__id=plan.rtqm_mt.planing.line.id,
            entry_date=current_date
        ).values()
        
        defect_counts = today_total_defect.values('defect','defect_name').annotate(defect_count=Count('defect'))
        ob_detail_counts = today_total_defect.values('ob_detail','ob_name').annotate(ob_count=Count('ob_detail'))
        defect_list = []
        ob_detail_list = []
        for item in defect_counts:
            defect_name = item['defect_name']
            defect_count = item['defect_count']
            defect_list.append({
                'defect_name': defect_name,
                'defect_count': defect_count
            })
            # print(f"defect_counts {defect_name}: {defect_count} occurrences")
            
        for item in ob_detail_counts:
            ob_name = item['ob_name']
            ob_count = item['ob_count']
            ob_detail_list.append({
                    'ob_name': ob_name,
                    'ob_count': ob_count
                })
            # print(f"Ob Count {ob_name}: {ob_count} occurrences")
            
            
        
        front_image_url = silhouettes_data.front_image.url if silhouettes_data.front_image else ''
        back_image_url = silhouettes_data.back_image.url if silhouettes_data.back_image else ''

        list_defect = list(today_total_defect)
        return {
            'silhouettes_data': {
                'front_image': front_image_url,
                'back_image': back_image_url
            },
            'today_defect_list': list_defect,
            'plan_data': {
                'id': plan_data.id,
                'buyer': plan_data.buyer_name,
                'style' :plan_data.styleno,
                'color':plan_data.color  ,
                'line': plan_data.line.name
            },
            'defect_list' :defect_list,
            'ob_list' :ob_detail_list
        }

        
        