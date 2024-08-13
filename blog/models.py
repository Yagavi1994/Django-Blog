from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))
CATEGORY = ((0, "Fiction"), (1, "Non-Fiction"))
GENRES = [
    (0, "Adventure"), 
    (1, "Romance"), 
    (2, "Fantasy"), 
    (3, "Science"), 
    (4, "Mystery"), 
    (5, "Horror"), 
    (6, "Thriller"), 
    (7, "Historical"), 
    (8, "Comedy"), 
    (9, "Drama"), 
    (10, "Detective/Crime"), 
    (11, "Western"), 
    (12, "Biography/Autobiography"), 
    (13, "Gothic"), 
    (14, "Dystopian"), 
    (15, "Epic"), 
    (16, "Coming-of-Age"), 
    (17, "Slice of Life"), 
    (18, "Tragedy"), 
    (19, "Mythology"),
    (20, "Technology"),
]

# Create your models here.

class Post(models.Model):
    """
    Stores a single blog post entry related to :model: `auth:user`
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    category = models.IntegerField(choices=CATEGORY, default=0)
    genre = models.IntegerField(choices=GENRES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title} | written by {self.author}"

class Comment(models.Model):
    """
    Store a single comment entry related to :model: `auth:user` and :model: `auth:blog.Post`.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

    