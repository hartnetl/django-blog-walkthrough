from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post


# First we want to generate a list of our posts for the user
class PostList(generic.ListView):
    # We want to use the Post model
    model = Post
    # queryset is the contents of our Post table
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # This is the file our view will render
    template_name = 'index.html'
    # limits posts to 6 per page, and auto navigation is enabled
    paginate_by = 6


class PostDetail(View):
    # This isn't a generic view, so we have to do everything ourselves

    def get(self, request, slug, *args, **kwargs):
        # Filter posts to those with the status as 1 (published)
        queryset = Post.objects.filter(status=1)
        # Get the published post with the right slug we're looking for
        post = get_object_or_404(queryset, slug=slug)
        # Get the comments of that post
        comments = post.comments.filter(approved=True).order_by('created_on')
        # if user liked the post before, let that show
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # render it
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            },
        )
