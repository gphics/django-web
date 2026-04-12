from django.db import models

# Create your models here.

class Media(models.Model):

    # urls
    public_url = models.TextField(null=True)
    media_key = models.TextField(null=True)

    # pointers
    user_profile = models.OneToOneField("account.Profile", null=True, on_delete=models.CASCADE, related_name="media")
    circle = models.OneToOneField("transaction.Circle", null=True, on_delete=models.CASCADE, related_name="media")

    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.public_url