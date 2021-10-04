from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


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
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

    # Get data from form and assign it to a variable
        comment_form = CommentForm(data=request.POST)

        # our form has a method called 'is_valid' that returns a Boolean value
        # regarding whether the form is valid, as in  all the fields have been
        # completed or not. If it is valid, a comment has been  left and we
        # want to process it. 
        if comment_form.is_valid():
            # set email and username automatically from logged in user
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)

            # We need to assign the comment to a post before it can be committed
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        # render it
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # Check if the user has liked the post
        if post.likes.filter(id=request.user.id).exists():
            # If it has, remove the like
            post.likes.remove(request.user)
        else:
            # If it hasn't, add the like
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
