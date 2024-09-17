from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.middleware.csrf import rotate_token
from time import sleep


class Test(View):
    def get(self, request):
        return render(request, 'test.html')
    
    def post(self, request):
        demo = request.POST.get("demo")
        print('\n' , demo , '\n')
        sleep(2)
        return redirect('/access-armor/test/')

