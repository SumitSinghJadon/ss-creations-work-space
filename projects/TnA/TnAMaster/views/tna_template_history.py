from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from App_db.models import TnaTemplateMt 


class TnaTemplateHistoryView(View):
    def get(self, request):
          template_data = TnaTemplateMt.objects.all()
          flag = request.GET.get("flag")
          
          if flag == 'approve':
               at_id = request.GET.get("id")
               TnaTemplateMt.objects.filter(id=at_id).update(status = 'approved')
               messages.success(request, "Template Status Approved")
            

          context = {
               'template_data': template_data,
          }

          return render(request, 'T&A_Template_History.html', context)
