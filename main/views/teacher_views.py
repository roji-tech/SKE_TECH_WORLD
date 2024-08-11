from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView


class TeachersHome(View):
    def get(self, request, *args, **kwargs):
        # Custom logic here
        return render(request, "teachers/index.html")


def uploadgmeet(request):
    return render(request, 'updated/gmeet/gmeet.html')

def editgmeet(request):
    return render(request, 'updated/gmeet/uploadgmeet.html')