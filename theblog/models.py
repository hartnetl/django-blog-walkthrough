from django.db import models
# Import user model
from django.contrib.auth.models import User
# Import cloudinary for featured image
from cloudinary.models import CloudinaryField

# Create tuple for published/draft status of blog
STATUS = ((0, "Draft"), (1, "Published"))


# Using E-R-D (relationship diagram), convert diagram into usable Django model
# link to onenote notes on this:
# https://onedrive.live.com/view.aspx?resid=AD7F40F390B59989%2110781&id=documents&wd=target%28blog%20walkthrough.one%7C871F9988-9AC4-4DB3-9672-E970CEC05F40%2FModels%20and%20admin%7C543D8EA0-8521-4270-B5C0-6FE9305720C4%2F%29

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    # excerpts visible on index page
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        # - here uses descending order
        ordering = ['-created_on']

    # This is a must. Returns a string representation of an object
    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

