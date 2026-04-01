from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-created_at"]
        indexes= [models.Index(fields = ["-created_at"])]

    def __str__(self):
        return self.title



class Transaction(models.Model):

    # ENUM FOR TRANSACTION TYPE
    class TRANSACTION_TYPE_ENUM(models.TextChoices):
        DEBIT = "DEBIT", "debit"
        CREDIT = "CREDIT", "credit"

        
    amount = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null = True)
    flagged = models.BooleanField(default=False)
    
    # date time info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # adding transaction type
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_ENUM, default=TRANSACTION_TYPE_ENUM.DEBIT)


    # adding transaction location information
    # country, state, city -> For subsetting all transactions within those locations
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes= [
            models.Index(fields=["country", "state", "city"]),
            models.Index(fields = ["-created_at"])
            ]


class CircleMembership(models.Model):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OWNER = "OWNER", "Owner"
        MEMBER = "MEMBER", "Member"
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    circle = models.ForeignKey('Circle', on_delete= models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "circle")

class Circle(models.Model):
    """
    This model refers to group of users who wanna monitor their transactions together.

    The circleMembership model was used as a through or joint table between user 
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    members = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="circles", through='CircleMembership')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"])]

    def update_member(self,user, role="MEMBER"):
        """
        This method is responsible for creating member or updating member role.
        """
        membership, created = CircleMembership.objects.update_or_create(
            circle = self,
            user = user,
            defaults={"role": role}
        )

        return membership
    

    def remove_member(self, user):
        """
        This method is responsible for removing member
        """
        return CircleMembership.objects.filter(circle=self, user = user).delete()

    def is_admin(self, user):
        """
        The role of this method is authorization
        This method is responsible for checking if a user is an admin(admin or owner) or a member
        """
        return CircleMembership.objects.filter(
            circle = self,
            user = user,
            role__in=["ADMIN", "OWNER"]
        ).exists()

    def is_member(self, user):
        """
        The role of this method is to check if a user is a member(regardless of his/her role) of a cirlce
        """
        return CircleMembership.objects.filter(
            circle = self,
            user = user,
            role__in = ["ADMIN", "OWNER", "MEMBER"]
        ).exists()
    
    def verify_member_role(self, user, role="MEMBER"):
        return CircleMembership.objects.filter(
            circle = self,
            user = user,
            role = role
        ).exists()

