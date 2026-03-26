from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Transaction, Circle, CircleMembership
from rapidfuzz import process as text_processor, fuzz
from babel.numbers import get_currency_symbol
from account.models import Profile

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    """"
    This serializer is for the creation of the user only
    """
   
    class Meta:
        model = User
        fields = "__all__"
        # fields = ["password", "username"]
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password length must be greater than 5")
        return value
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class TransactionReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
 
    class Meta:
        model = Transaction
        fields = "__all__"
        depth = 1


class ShallowTransactionReadSerializer(serializers.ModelSerializer):
    """
    This serializer handle reading the transactions without going too deep (getting field data e.g user data).
    """

    user = serializers.CharField(source = "user.username", read_only = True)
    category = serializers.CharField(source = "category.title", read_only = True)

    
    class Meta:
        model = Transaction
        fields = "__all__"
     
        
class TransactionCreationSerializer(serializers.ModelSerializer):
    """
    This serializer is for creating and updating the transaction
    """
    
    class Meta:
        model = Transaction
        fields = "__all__"
        

    def validate(self,attrs):
        """
        This validation method ensures that the user profile have the location info (state, city and country) as they are needed on the transaction instance
        """
        auth_user = self.context["request"].user

        city = auth_user.profile.city
        state = auth_user.profile.state
        country = auth_user.profile.country

        if not city:
            raise serializers.ValidationError("Please update the city on your profile before making a transaction")
        if not state:
            raise serializers.ValidationError("Please update the state on your profile before making a transaction")
        if not country:
            raise serializers.ValidationError("Please update the country on your profile before making a transaction")
        return attrs

    def create(self, validated_data):
        """
        Overiding the create method of the transaction model
        """
        auth_user = self.context["request"].user

        # adding location info to validated data

        validated_data["city"] = auth_user.profile.city
        validated_data["state"] = auth_user.profile.state
        validated_data["country"] = auth_user.profile.country

        # saving the data
        return super().create(validated_data)
    

    
# 
# 
# All about circle

class CircleSerializer(serializers.ModelSerializer):
    """
    This serializer if for circle creation
    """
    class Meta:
        model = Circle
        fields = "__all__"



class CircleMemberProfileSerializer(serializers.ModelSerializer):
    """
    A specially made profile serializer for circle
    """
  
    class Meta:
        model = Profile
        exclude = ["user"]

class CircleMemberSerializer(serializers.ModelSerializer):
    """
    A specially made user serializer for circle. it automatically add profile
    """
    profile = CircleMemberProfileSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'last_login']

        
class CircleListSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Circle
        fields = "__all__"


    def get_members(self, obj):
        memberships = CircleMembership.objects.filter(circle = obj)

        return [
            {
                "user":CircleMemberSerializer(m.user).data,
                "role":m.role,
                "joined_at":m.joined_at
            }
            for m in memberships
        ]
