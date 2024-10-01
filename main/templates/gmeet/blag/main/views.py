from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
# Create your views here.
# from django.views import View
from .models import BlogPost
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# @method_decorator(login_required(login_url="/login"), name='dispatch')
class BlogListView(ListView):
    template_name = "blogs/index.html"
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        queryset = BlogPost.objects.filter(user=user)
        print(user)
        return queryset


# def blog_list_view(request):
#     queryset = BlogPost.objects.all()
#     user = request.user
#     return render(request, "blogs/index.html", {})
