![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# A break down of the steps in each lesson for building this blog

<details>
<summary></summary>

</details>


<details>
<summary><h1>LESSON 1: USER STORIES</h1></summary>

* Use github projects as your kanban board
* Set automation for 'issues' to 'todo'
* Create user stories in issues, making sure to select the project to send them to

* User stories should fill in:
    * As a * role * I can * capability* so that * received benefit *
* Try consider this from the aspect of site user and site owner

### This blog example

    • Site pagination: As a site user I can view a paginated list of posts so that I can easily select a post to view
	• View post list: As a Site User I can view a list of posts so that I can select one to read
	• Open a post: As a Site User I can click on a post so that I can read the full text
	• View likes: As a Site User / Admin I can view the number of likes on each post so that I can see which is the most popular or viral
	• View comments: As a Site User / Admin I can view comments on an individual post so that I can read the conversation
	• Account registration: As a Site User I can register an account so that I can comment and like
	• Comment on a post: As a Site User I can leave comments on a post so that I can be involved in the conversation
	• Like / Unlike: As a Site User I can like or unlike a post so that I can interact with the content
	• Manage posts: As a Site Admin I can create, read, update and delete posts so that I can manage my blog content
	• Create drafts: As a Site Admin I can create draft posts so that I can finish writing the content later
    • Approve comments: As a Site Admin I can approve or disapprove comments so that I can filter out objectionable comments  

</details>

<details><summary><h1>LESSON 2 - CREATING AND DEPLOYING EMPTY PROJECT</h1></summary>

[CI videos](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+FST101+2021_T1/courseware/b31493372e764469823578613d11036b/9236975633b64a12a61a00e0cca7c47d/?child=first)  

<details>
<summary><h2>LESSON 2.1 - DJANGO PROJECT CHECKLIST</h2></summary>
<hr>

[source code](https://github.com/Code-Institute-Solutions/Django3blog/tree/master/01_creating_the_project)  
[Django setup cheat sheet](https://codeinstitute.s3.amazonaws.com/fst/Django%20Blog%20Cheat%20Sheet%20v1.pdf)  

The four steps to setting up a new project:  
1. install django and the supporting libraries
2. create new, blank Django project and app 
3. Set our project to use cloudinary and postgreSQL
4. Deploy our new empty project to heroku

</details>

<details>
<summary><h2>LESSON 2.2 - CREATING EMPTY DJANGO PROJECT </h2></summary>
<hr>

Go to your empty project terminal

Install django and required libraries  

*  pip3 install django gunicorn  
gunicorn is the server used by heroku to run django  
*  pip3 install dj_database_url psycopg2  
dj database is needed for postgres  
psycopg2 is needed for python  
* pip3 install dj3-cloudinary-storage  
cloudinary is for our images  
* pip3 freeze --local > requirements.txt  
Get requirements file for heroku  

Create django project  

* django-admin startproject myblog .

Create blog app

* python3 manage.py startapp theblog

myblog -> settings.py
* Add 'theblog' to the installed_apps

migrate changes to database (using terminal)
* python3 manage.py migrate

The project should have been successfully built. Check with  
* python3 manage.py runserver


</details>

<details>
<summary><h2>LESSON 2.3 + 2.4 - FIRST DEPLOYMENT</h2></summary>
<hr>

**Error fix**  
If you get the error below during the steps to deployment:  

django.db.utils.OperationalError: FATAL: role "somerandomletters" does not exist  

Please run the following command in the terminal to fix it:  

**unset PGHOSTADDR**  

<hr>

There are 4 steps to deploying an app to heroku

1. Create app on heroku
2. Attach PostgreSQL database
3. Prepare environment and settings.py files
4. Get our static and media files stored on Cloudinary  


**Create app on heroku**

* Go to heroku.com  
* Create an app for the eu  

**Attach postgres database**

* Resources tab on heroku
    * Search postgres
    * Pick heroku postgres and attach  

**Prepare gitpod environment**

* Get postgres URL from heroku
    * Settings
    * Reveal config vars
    * copy database url

Back to gitpod

* Create env.py folder in root directory
    * import os  
    os.environ["DATABASE_URL"] = "THE_LINK_YOU_JUST_COPIED_FROM_HEROKU"  
    os.environ["SECRET_KEY"] = "makeOneUp"  

* Add that secret key to heroku under config vars.  

* settings.py
    * Some imports for underneath the first one
        * import os   
        import dj_database_url  
        if os.path.isfile('env.py'):  
            import env  
    * secret key section
        * Change it to 
            * SECRET_KEY = 'os.envrion.get('SECRET_KEY')

Let's wire up the postgres database  

* settings.py
    * DATABASE_URL
        * Comment out existing DATABASE
        * Create another below as so
            * DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

* Run migrations again and it should run. Check the postgres link under resources and 48 lines should have been created

**Connect cloudinary**

Cloudinary Setup
* Visit the [Cloudinary website](https://cloudinary.com/)
* Click on the Sign Up For Free button
* Provide your name, email address and choose a password
* For Primary interest, you can choose Programmable Media for image and video API
* Optional: edit your assigned cloud name to something more memorable
* Click Create Account
* Verify your email and you will be brought to the dashboard

Link to cloudinary  

* Copy your api environment variable from the dashboard
* Go to env.py 
    * os.environ["CLOUDINARY_URL"] = "the_link_you_just_copied_without_the_first_bit"
* Go to config vars on heroku
    * Cretae cloudinary URL with your copied link
    * Create temporary variable
        * DISABLE_COLLECTSTATIC = 1
* settings.py
    * Installed apps
        * 'cloudinary_storage',    
        Above static files
        * 'cloudinary',    
        Below static files
    * Under STATIC_URL
        * STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'  
        STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  
        STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  
        MEDIA_URL = '/media/'  
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'   

Tell Django where our templates will be 

* settings.py
    * under BASE_DIR
        * TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    * TEMPLATES
        * 'DIRS': [TEMPLATES_DIR]

Add to allowed hosts

* settings.py
    * ALLOWED_HOSTS = ['django-blog-walkthrough.herokuapp.com', 'localhost']  

Create 'static', 'media' and 'templates' folders in the main root directory  

Create Procfile   
* web: gunicorn myblog.wsgi

Go to heroku   
* Deploy tab
* connect to github and the repository for the project
* Enable Automatic Deploys
* Deploy branch


**note**  
When I did this I got an error and when I checked the heroku logs it was a h10 error in relation to favicons.
In the end I missed some commas in installed apps. 
so BE CAREFUL

</details>

</details>



<details>
<summary><h1>LESSON 3: MODELS AND ADMIN</h1></summary>

[CI videos](https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+FST101+2021_T1/courseware/b31493372e764469823578613d11036b/09e0a94c7dbd4b969b8358a0cf5660b2/?child=first)

Remember Django runs on a MTV framework.  
M - model - database and structure  
T - template - html pages our user sees  
V - views - the logic that connects the two. The logic in our code that reads from or updates the model and then updates what the user sees.

<details>
<summary><h2>LESSON 3.1: Creating Database Diagram</h2></summary>
<hr>

* Move 3 of the user stories to user stories: manage posts, create drafts and approve comments
* Build relationship model for database. Imagine a blogpost, and the data you'll need for it  
[link to onenote notes on this](https://onedrive.live.com/view.aspx?resid=AD7F40F390B59989%2110781&id=documents&wd=target%28blog%20walkthrough.one%7C871F9988-9AC4-4DB3-9672-E970CEC05F40%2FModels%20and%20admin%7C543D8EA0-8521-4270-B5C0-6FE9305720C4%2F%29)

</details>

<details>
<summary><h2>LESSON 3.2: Creating Database Models</h2></summary>
<hr>

**Note:** If you're concerned that you may have made a typing error, then you can do a dry run of your migrations before you apply them to your database. The command to do this is:

python3 manage.py makemigrations --dry-run

This will print out the migrations, so you can check that everything is correct before proceeding.

<hr>

* models.py
    * Create models for posts and comments  

    from django.db import models  
    from django.contrib.auth.models import User  
    from cloudinary.models import CloudinaryField  

        STATUS = ((0, "Draft"), (1, "Published"))  

        class Post(models.Model):  
            title = models.CharField(max_length=200, unique=True)  
            slug = models.SlugField(max_length=200, unique=True)  
            author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")  
            updated_on = models.DateTimeField(auto_now=True)  
            content = models.TextField()  
            featured_image = CloudinaryField('image', default='placeholder')  
            excerpt = models.TextField(blank=True)  
            created_on = models.DateTimeField(auto_now_add=True)  
            status = models.IntegerField(choices=STATUS, default=0)  
            likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)  

        class Meta:  
            ordering = ['-created_on']  

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


* migrate change to database
    * python3 manage.py makemigrations
    * python3 manage.py migrate

**note** If you make changes to this model, you'll have to make these migrations again  



</details>

<details>
<summary><h2>LESSON 3.3 + 3.4 : Building the admin site</h2></summary>
<hr>

[django list view](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.changelist_view)
[django search fields](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)
[summernote](https://summernote.org/)
[source code](https://github.com/Code-Institute-Solutions/Django3blog/tree/master/05_building_the_admin_site)

<hr>

create a superuser for the django admin panel
 
 * Terminal
    * python3 manage.py createsuperuser
* Test it 
    * python3 manage.py runserver
    * Add "/admin" to the end of the url
    * Sign in with the credentials you just made

Add post model to admin panel 

* admin.py
    * from django.contrib import admin  
from .models import Post  
admin.site.register(Post)  

You can now create posts in your admin panel  

We're going to use a WYSIWYG or "what you see is what you get" editor for the post.  
We're going to use a handy  library called Summernote. 

* Terminal
    * pip3 install django-summernote
    * pip3 freeze --local > requirements.txt
* Add summernote to settings.py under INSTALLED_APPS, right above theblog
    * 'django_summernote',
* Set up summernote in urls.py
    * add include to the django.urls import
    * Add this to the urlpatterns
        * path('summernote/', include('django_summernote.urls')),
* Tell admin panel which field we want to use summernote for
    * admin.py
        * from django_summernote.admin import SummernoteModelAdmin  
        class PostAdmin(SummernoteModelAdmin):  
        summernote_fields = ('content')  
* Register post admin to our admin site
    * admin.py
        * delete "admin.site.register(Post)"
        * Add decorator to PostAdmin class
            * @admin.register(Post)
            * this will register both our post model and the post admin class with our admin site.


</details>
</details>