from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import User
from Task.models import TaskForwardMt, TaskMasterMt
from django.contrib import messages


class TaskForward(View):
    def get(self, request):
        user_list = User.objects.using('is_main_db').filter(is_active=True)
        task_list = TaskMasterMt.objects.filter(is_active=True, status='pending')

        context = {
            'user_list' : user_list,
            'task_list' : task_list,
        }
        return render(request, 'task_forward.html', context)
    
    def post (self, request):
        task = request.POST.getlist('task')
        forward_to = request.POST.getlist('forward_to')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        task = TaskForwardMt.objects.create(
            task = task,
            forward_to = forward_to,
            start_time = start_time,
            end_time = end_time,
        )

        messages.success(request, "Success! The entry has been created.")
        return redirect ('task_forward_page')