from . import views
from django.urls import path


urlpatterns = [
    # a blank path is the default link, so the home page
    # .as_view() renders the class PostList as a view
    path('', views.PostList.as_view(), name='home')
]