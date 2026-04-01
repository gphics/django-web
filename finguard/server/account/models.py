from django.db import models
from django.conf import settings



# Create your models here.
class Profile(models.Model):
    class FINANCIAL_ACTIVITY_ENUM(models.TextChoices):
        CONSISTENT = "CONSISTENT", "Very Consistent"
        MODERATE = "MODERATE", "Fairly Regular"
        FLUNCTUATING = "FLUNCTUATING","Flunctuating"

    class USER_TYPE_ENUM(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "individual"
        ENTREPRENEUR = "ENTREPRENEUR", "entrepreneur"

    financial_activity = models.CharField(max_length=30,choices=FINANCIAL_ACTIVITY_ENUM, default=FINANCIAL_ACTIVITY_ENUM.CONSISTENT)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=20, choices=USER_TYPE_ENUM, default=USER_TYPE_ENUM.INDIVIDUAL)
    
    # country, state, city -> Used for transaction creation
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)

    # handling currency
    currency = models.CharField(max_length=10, default = "$")
    
    contact = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # this field are updated once a new transaction is created
    summary_statistics = models.JSONField(null=True, default=None)
    number_of_transactions = models.IntegerField(default = 0)
    class Meta:
        ordering = ["-created_at"]
        indexes= [models.Index(fields = ["-user_id"])]
       

    def __str__(self):
        return self.user.username
    
