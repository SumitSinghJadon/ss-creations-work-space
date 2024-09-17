from django.views import View
from django.shortcuts import redirect, render
from IntelliSync_db.models import User


class UserList(View):
    def get(self, request):
        user_list = User.objects.all()
        context = { 'user_list' : user_list }
        return render(request, 'user_list.html', context)

