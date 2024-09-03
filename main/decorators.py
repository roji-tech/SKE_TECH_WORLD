from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

def admin_is_authenticated(*args):
    # print(args)I
    return method_decorator(login_required(login_url="/admin/login/"), name='dispatch')


def student_is_authenticated(*args):
    
    return method_decorator(login_required(login_url="/admin/login/"), name='dispatch')
