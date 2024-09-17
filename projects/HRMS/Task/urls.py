from django.urls import path
from Task.views import TaskMaster, TaskForward

urlpatterns = [
    path('taskmaster/', TaskMaster.as_view(), name='task_master_page'),
    path('taskforward/', TaskForward.as_view(), name='task_forward_page')
]