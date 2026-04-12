from django.db import models

# Create your models here.
class TimeDelta(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-updated_at"]



class Post(TimeDelta):
    author = models.CharField(max_length=25)
    content = models.TextField()


    def __str__(self):
        return f"post_{self.pk} by {self.author} on {self.content[:10]} ..."


class Comment(TimeDelta):
    messages = models.JSONField(null=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

class Like(TimeDelta):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"liked a comment from post {self.comment.post.id} "