from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Transaction, Circle, CircleMembership
from rapidfuzz import process as text_processor
from babel.numbers import get_currency_symbol
from account.models import Profile
from media_app.serializers import MediaSerializer
from account.serializers import UserSerializer
User = get_user_model()

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
    category = serializers.CharField(write_only=True)
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
        Overriding the create method
        """

        # ATTTENDING TO THE CATEGORY FIELD
        category_input = validated_data.pop("category")

        # if id is provided
        if category_input.isdigit():
            category = Category.objects.filter(id = int(category_input))

            if not category.exists():
                raise serializers.ValidationError("Category id provided does not exist")
            else:
                category = category[0]
        
        # if title was provided
        else:
            # getting all categories
            all_categories = Category.objects.all()

            # getting counts
            categories_count = all_categories.count()

            # if transaction categories is empty
            if  categories_count < 1:
                # creating new category
                category = Category.objects.create(title=category_input)
                
            else:
                all_categories_list = [ cat.title for cat in all_categories]
                
                # getting category with the closest similar title
                result= text_processor.extractOne(category_input, all_categories_list, score_cutoff=80)
                    
                # if best match found 
                if result:
                    title, *rest = result
                    category = all_categories.filter(title = title)[0]
                else:      
                    # creating new category if best match is not found
                    category = Category.objects.create(title=category_input)
                    
        # adding category to validated data
        validated_data["category"] = category

        # HANDLING THE TRANSACTION LOCATION

        # getting auth user
        auth_user = self.context["request"].user

        # adding location info to validated data
        validated_data["city"] = auth_user.profile.city
        validated_data["state"] = auth_user.profile.state
        validated_data["country"] = auth_user.profile.country

        return super().create(validated_data)

    def update(self,instance, validated_data):
        """
        Overiding the update method
        """

        category_input = validated_data.pop("category")

        if category_input.isdigit():
            category = Category.objects.filter(id = category_input)

            # validating the category
            if not category.exists():
                raise serializers.ValidationError("Category id provided does not exist")
            else:
                category = category[0]

        # if title was provided
        else:
            # getting all categories
            all_categories = Category.objects.all()

            # getting counts
            categories_count = all_categories.count()

            # if transaction categories is empty
            if  categories_count < 1:
                # creating new category
                category = Category.objects.create(title=category_input)
                
            else:
                all_categories_list = [ cat.title for cat in all_categories]
                
                # getting category with the closest similar title
                result= text_processor.extractOne(category_input, all_categories_list, score_cutoff=80)
                    
                # if best match found 
                if result:
                    title, *rest = result
                    category = all_categories.filter(title = title)[0]
                else:      
                    # creating new category if best match is not found
                    category = Category.objects.create(title=category_input)
                    
        # adding category to validated data
        validated_data["category"] = category

        return super().update(instance, validated_data)
    

    
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
    A specially made profile serializer for circle. It exclude the user field on the profile
    """
    media = MediaSerializer(read_only = True)
    class Meta:
        model = Profile
        exclude = ["user"]

class CircleMemberSerializer(serializers.ModelSerializer):
    """
    A specially made user serializer for circle. It add the profile field to the user object returned using the custom profile serializer created earlier.
    """
    profile = CircleMemberProfileSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'last_login']

        
class CircleListSerializer(serializers.ModelSerializer):
    """
    This serializer is for reading the circle object and it goes deep to bring out the details of the members of a circle
    """
    members = serializers.SerializerMethodField()
    media = MediaSerializer(read_only = True)
    class Meta:
        model = Circle
        fields = "__all__"


    def get_members(self, obj):
        memberships = CircleMembership.objects.filter(circle = obj)

        members_data =  [
            {
                "user":CircleMemberSerializer(m.user).data,
                "role":m.role,
                "joined_at":m.joined_at
            }
            for m in memberships
        ]

        return self.sort_by(data=members_data)

        # sorted_by_mean = sorted(
        #     members_data,
        #     key= lambda x: x["user"]["profile"]["summary_statistics"].get("mean", 0),
        #     reverse=True
        # )
        
        # # adding rank
        # for index, member in enumerate(sorted_by_mean):
        #     member["rank"] = index + 1

        # return sorted_by_mean
    
    def sort_by(self,data, summ_stat_param:str="mean"):
        """
        This method sort circle members base on a provided summ_stat_param with the default beign mean.
 

        Return:
            sorted members
        """

        members = data 
        acceptable_param = ["mean", "std", "min", "count", "max"]

        # verifying if summ_stat_param provided is acceptable
        if summ_stat_param not in acceptable_param:
            raise serializers.ValidationError("The summary statistics param provided is not acceptable")
        
        sorted_members_data = sorted(
            members,
            key= lambda x:x["user"]["profile"]["summary_statistics"].get(summ_stat_param, 0),
            reverse=True
        )

        # adding rank
        for index, member in enumerate(sorted_members_data):
            member["rank"] = index + 1

     
        return sorted_members_data