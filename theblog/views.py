from django.shortcuts import render
from django.views import generic
from .models import Post


# First we want to generate a list of our posts for the user
class PostList(generic.ListView):
    We want to use the Post model
    model = Post
    # queryset is the contents of our Post table
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # This is the file our view will render
    template_name = 'index.html'
    # limits posts to 6 per page, and auto navigation is enabled
    paginate_by = 6

