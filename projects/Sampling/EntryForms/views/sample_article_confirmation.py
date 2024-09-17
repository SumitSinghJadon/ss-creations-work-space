from django.views import View
from django.shortcuts import render

class SampleArticleConfirmationView(View):
    def get(self, request):
        article_breakup_list = [1,2,3,4,5,6]
        context = {
            'article_breakup_list' : article_breakup_list
        }
        return render(request, 'sample_article_confirmation.html', context)    