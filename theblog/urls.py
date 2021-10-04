from . import views
from django.urls import path


urlpatterns = [
    # a blank path is the default link, so the home page
    # .as_view() renders the class PostList as a view
    path('', views.PostList.as_view(), name='home'),
    # the first slug is a path converter, the second is a keyword name.
    # the slug keyword name matches the slug parameter in the get method of the
    # PostDetail class in the theblog/views.py file. That's how we link them
    # together.
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),

]
