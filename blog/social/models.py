from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

class STATUS(models.IntegerChoices):
        DRAFT = 1, _("DRAFT")
        PUBLISHED = 2, _("PUBLISHED")


class DraftManager(models.Manager):
    
    def get_queryset(self):
         return super().get_queryset().filter(status=1)

# Create your models here.
class Post(models.Model):
    objects = models.Manager()
    drafted = DraftManager()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique_for_date="created")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.DRAFT)
    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"])
        ]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("social:post_detail", args=[self.created.year,self.created.month, self.created.day, self.slug])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300)

    class Meta:
          ordering = ["-created"]
          indexes = [
               models.Index(fields=["-created"])
          ]

    def __str__(self):
          return "{} commented on {}".format(self.name, self.post)
     
