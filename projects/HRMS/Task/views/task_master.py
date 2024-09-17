from django.views import View
from django.shortcuts import render, redirect
from Task.models import TaskMasterMt
from IntelliSync_db.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages


class TaskMaster(View):
    def get (self, request):
        user_list = User.objects.filter(is_active=True)
        frequency_list = TaskMasterMt.frequency_list
        priority_list = TaskMasterMt.priority_list
        context = {
            'user_list' : user_list,
            'frequency_list' : frequency_list,
            'priority_list' : priority_list
        }
        return render(request, 'task_master.html', context)
    
    def post (self, request):
        users = request.POST.getlist("user")
        title = request.POST.get('title')
        description = request.POST.get('description')
        owner = request.POST.get('owner')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        frequency = request.POST.get('frequency')
        priority = request.POST.get('priority')
        # remainder = request.POST.get('remainder')
        remarks = request.POST.get('remarks')

        owner = User.objects.using('is_main_db').get(id=owner)
        users = User.objects.using('is_main_db').filter(id__in=users, is_active=True)

        task = TaskMasterMt.objects.create(
            title = title,
            description = description,
            owner = owner,
            start_time = start_time,
            end_time = end_time,
            frequency = frequency,
            priority = priority,
            # remainder = remainder,
            remarks = remarks,
            created_by = request.user
        )

        for user in users:
            task.user.add(user)

        messages.success(request, "Success! The entry has been created.")
        return redirect ('task_master_page')

