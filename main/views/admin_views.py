from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView


class AdminsHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "myadmin/index.html")
