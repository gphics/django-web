
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, ProfileSerializer, CategorySerializer,TransactionReadSerializer,TransactionCreationSerializer, CircleListSerializer, CircleSerializer
from .models import Profile, Category, Transaction, Circle
from django.db import transaction
from .res import generate_res
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rapidfuzz import process as text_processor, fuzz
from utils import DataTransformationEngine, DataInterpretationEngine
from babel.core import get_global


# 
# 
#  USER (AUTH) ...

@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    """
    This is the user and default profile creation view. It 

    Request Data:
        username
        password
    Return:
        It return the user auth token
    """

    # verifying if auth user already exists
    if request.user.is_authenticated:
        return Response(generate_res(err={"msg":"You are already authenticated"}))
    
    # creating serializer
    serializer = UserSerializer(data = request.data)

    if serializer.is_valid():
        # creating atomic transaction to make sure the two process was successful
        with transaction.atomic():
            user = serializer.save()
            Profile.objects.create(user = user)

            token = Token.objects.get_or_create(user = user)
            
           
        return Response(generate_res({"msg":{
            "token":str(token[0])
        }}))
    # print(serializer.errors)
    return Response(generate_res(err={"msg" : serializer.errors}), status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def auth_user(request):
    """
    The login view

    Request Data:
        username
        password

    Return:
        auth token
    """
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if not username or not password:
        return Response(generate_res(err={"msg":"password and username must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password = password)
    if user:
        token = str(Token.objects.get_or_create(user = user)[0])

        return Response(generate_res({"token":token}))
    return Response(generate_res(err={"msg":"invalid credentials"}), status=status.HTTP_400_BAD_REQUEST)

#
#
# PROFILE ...

class ProvileView(APIView):
    """
    This class view handles all CRUD ops for both profile and user model
    """
    def get(self, request):
        """
        This is the read view. It get the profile data of the logged in user

        Request param:
            search (optional): user id (int) | all (to get all users)

        Return:
            user(s) profile
        """
        search = request.query_params.get("search", None)
        if not search:
            user = request.user
            serializer = ProfileSerializer(instance = Profile.objects.get(user = user))
            
        elif search == "all":
            serializer = ProfileSerializer(instance = Profile.objects.all(), many = True)
        else:
            try:
                user = User.objects.get(pk = int(search))
            except Exception as e:
                return Response(generate_res(err={"msg": str(e)}), status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(instance = Profile.objects.get(user = user))
        return Response(generate_res({"msg":serializer.data}))

    def put(self, request):
        """
        This is update route for basic information update for profile and user. email, username and password cannot be changed here.
        """

        # previous user info
        req_user = request.user
        req_profile = Profile.objects.get(user = req_user)

        # selecting the data from the request object
        user = request.data.get("user", {})
        profile = request.data.get("profile", {})

        # filtering out email and username
        if user.get("username") or user.get("email"):
            return Response(generate_res(err={"msg":"action not allowed"}), status=status.HTTP_400_BAD_REQUEST)

        # serializers
        user_ser = UserSerializer(instance = req_user, data = user, partial = True)
        profile_ser = ProfileSerializer(instance = req_profile, data = profile, partial = True)
        
        # validating and saving
        if user_ser.is_valid() and profile_ser.is_valid():
            with transaction.atomic():
                user_ser.save()
                profile_ser.save()
            return Response(generate_res(data={"msg": "user profile updated successfully"}))
        else:
            return Response(generate_res(err={user_ser.errors or None, profile_ser.errors or None}), status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_all_currencies(request):
    """
    This view returns all currencies codes and symbols

    """

    all_currencies = get_global("all_currencies")

    return Response(generate_res({"msg": all_currencies}))
    
@api_view(["PUT"])
def update_password(request):
    """
    This view is for updating the password

    Request data:
        old_password
        new_password

    Return:
        auth token
    """
    user = request.user
    old_password  =  request.data.get("old_password", None)
    new_password  =  request.data.get("new_password", None)

    # validations
    if not old_password or not new_password:
        return Response(generate_res(err={"msg":"Both old and new password must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    if len(str(new_password)) < 6:
        return Response(generate_res(err={"msg":"New password length must be greater than 5"}), status=status.HTTP_400_BAD_REQUEST)
    
    # making sure the old password provided is the actual previous password
    is_old_password = user.check_password(old_password)

    # making sure the new password is not the same with the old password
    is_password_unavailable = user.check_password(new_password)
    
    if not is_old_password:
        return Response(generate_res(err={"msg":"The old password is not correct"}), status=status.HTTP_400_BAD_REQUEST)
    
    if is_password_unavailable:
        return Response(generate_res(err={"msg":"The old password and new password must be different"}), status=status.HTTP_400_BAD_REQUEST)
    
    # saving the new password
    user.set_password(str(new_password))
    user.save()
    
    return Response(generate_res({"msg":"password updated successfully"}))


@api_view(["PUT"])
def update_username(request):
    """
    This view is for updating the username

    Request data:
        username
    Return:
        auth token
    """
    username = request.data.get("username", None)
    if not username:
        return Response(generate_res(err={"msg":"username must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    
    # checking email availability
    is_unavailable = User.objects.filter(username = username).exists()
    if is_unavailable:
        return Response(generate_res(err={"msg":"user already exist"}), status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    user.username = username
    user.save()

    return Response(generate_res({"msg":"username updated successfully"}))

@api_view(["PUT"])
def update_email(request):
    """
    This view is for updating the user email

    Request data:
        email

    Return:
        auth token
    """
    email = request.data.get("email", None)
    if not email:
        return Response(generate_res(err={"msg":"email must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    
    # checking email availability
    is_unavailable = User.objects.filter(email = email).exists()
    if is_unavailable:
        return Response(generate_res(err={"msg":"user already exist"}), status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    user.email = email
    user.save()

    return Response(generate_res({"msg":"email updated successfully"}))
# 
# 
# CATEGORY...

class CategoryCRUDView(APIView):

    def get(self, request):
        """
        This route returns all categories
        """
        serializer = CategorySerializer(instance = Category.objects.all(), many = True)
        return Response(generate_res({"msg": serializer.data}))
       
       
    def post(self, request):
        """
        This is the creation view for the category creation
        """
        title = request.data.get("title", None)

        # for forcibly creating the category if a similar category already exist
        force = request.query_params.get("force", None)

        # if title was not provided
        if not title:
            return Response(generate_res(err={"msg":"category title is required"}), status=status.HTTP_400_BAD_REQUEST)
        
        # checking if a category with the same similar title already exist
        all_categories = [ cat.title for cat in Category.objects.all()]
        if len(all_categories):
            # getting category with the closest similar title
            best_match, score,_= text_processor.extractOne(title, all_categories)
            # terminating the operation if a best match with a score of >= 80 is found and force is not present
            if not force and (score >= 80):
                return Response(generate_res(err={"msg":f"category '{title}' already exist as '{best_match}' "}))
        try:
            Category.objects.create(title=title)
            return Response(generate_res({"msg":"category created"}))
        except Exception as e:
            return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
        


# 
# 
#  TRANSACTIONS ...

class TransactionCRUDView(APIView):
    """
    This class based view uses two serializers; one for creation and the other one for reading. I could have used one serializer but because I have two model fields that I wanna populate and might want to update and this would require tweeking and all sorts . so in order to make my code cleaner and easy to understand, I separated the logic.
    """

    def get(self, request):
        """
        This view is responsible for reading user transactions

        Request Query:
            id:int --> transaction id

        Return:
            If id, transaction with the id is returned else, it returns all user transactions.
        """
        transaction_id = request.query_params.get("id", None)
        try:
            if transaction_id:
                trans = Transaction.objects.filter(pk = transaction_id)
                if not trans.exists():
                    raise Exception("Transaction does not exist")
                serializer = TransactionReadSerializer(instance = trans[0])
            else:
                serializer = TransactionReadSerializer(Transaction.objects.filter(user = request.user), many=True)

  
              
            return Response(generate_res({"msg":serializer.data}))
        except Exception as e:
            return Response(generate_res(err={"msg": str(e)}), status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        
        """
        This view is responsible for creating transactions

        Request data:
            amount: int
            category: category id(int)
            transaction_date?: datetime(str)

        """

        serializer = TransactionCreationSerializer(data={**request.data, "user":request.user.pk})
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(generate_res({"msg":"transaction created"}))
        except Exception as e:
             return Response(generate_res(err={"msg": serializer.errors or str(e)}), status=status.HTTP_400_BAD_REQUEST)
       
        
    def put(self, request):
        """
        This view is for updating the transaction object

        """
        transaction_id = request.query_params.get("id", None)
        trans = Transaction.objects.filter(pk = transaction_id)
        if not trans.exists():
             return Response(generate_res(err={"msg": "transaction does not exist"}), status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionCreationSerializer(instance = trans[0], data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(generate_res({"msg":"transaction updated"}))
        
        return Response(generate_res(err={"msg": serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        This view is for deleting the transaction

        Request param:
            id : transaction id(int)
        """
        transaction_id = request.query_params.get("id", None)
        trans = Transaction.objects.filter(pk = transaction_id)
        if not trans.exists():
             return Response(generate_res(err={"msg": "transaction does not exist"}), status=status.HTTP_404_NOT_FOUND)
        trans.delete()
        return Response(generate_res({"msg":"transaction deleted"}))
    


@api_view(["GET"])
def interpret_summary_statistics(request):
    """
    This view is responsible for interpreting the summary statistics.
    Including:
        amount
        amount(deep)
        transaction_date

    Lastly, this function split transactions base on user location data if it exist.
        
    """

    # 
    # 
    # WORKING ON USER INTERPRETATIONS

    # getting all transactions
    all_transactions = TransactionReadSerializer(instance = request.user.transactions.all(), many = True)


    transformer = DataTransformationEngine(all_transactions.data)

    # json data of the summary_statistics
    json_data = {
        "amount": transformer.transform_amount(),
        "transaction_dates": transformer.transform_transaction_date(),
        "amount_by_date": transformer.transform_amount(deep=True)
    }
    interpreter = DataInterpretationEngine(json_data, currency=request.user.profile.currency, spending_pattern=request.user.profile.spending_pattern)

    user_interpretaions = interpreter.interpret_all()


    #
    #
     # WORKING ON LOCATION INTERPRETATIONS

    # getting auth user location data
    city = request.user.profile.city  or None
    state = request.user.profile.state or None
    country = request.user.profile.country  or None

    # Handling location statistics
    location_interpretations = []

    # if user profile have city
    if city:
        # serializing the data
        city_serializer = TransactionReadSerializer(instance = Transaction.objects.filter(user__profile__city = city), many = True)

        # initialising the data transformer
        transformer = DataTransformationEngine(city_serializer.data)

        # calculating the location summary statistics
        json_data = {"amount":transformer.transform_amount()}

        # initialising summary statistics interpreter
        interpreter = DataInterpretationEngine(json_data, currency=request.user.profile.currency, spending_pattern=request.user.profile.spending_pattern)

        # interpreting the summary statistics
        location_statistics = interpreter.interpret_location_amount(city)

        # appending ...
        location_interpretations.append(location_statistics)
    
    # if user profile have state
    if state:
        # serializing the data
        state_serializer = TransactionReadSerializer(instance = Transaction.objects.filter(user__profile__state = state), many = True)

        # initialising the data transformer
        transformer = DataTransformationEngine(state_serializer.data)

        # calculating the location summary statistics
        json_data = {"amount":transformer.transform_amount()}

        # initialising summary statistics interpreter
        interpreter = DataInterpretationEngine(json_data, currency=request.user.profile.currency, spending_pattern=request.user.profile.spending_pattern)

        # interpreting the summary statistics
        location_statistics = interpreter.interpret_location_amount(state, location_type="state")

        # appending ...
        location_interpretations.append(location_statistics)
    
    # if user profile have country
    if country:
        # serializing the data
        country_serializer = TransactionReadSerializer(instance = Transaction.objects.filter(user__profile__country = country), many = True)

        # initialising the data transformer
        transformer = DataTransformationEngine(country_serializer.data)

        # calculating the location summary statistics
        json_data = {"amount":transformer.transform_amount()}

        # initialising summary statistics interpreter
        interpreter = DataInterpretationEngine(json_data, currency=request.user.profile.currency, spending_pattern=request.user.profile.spending_pattern)

        # interpreting the summary statistics
        location_statistics = interpreter.interpret_location_amount(country, location_type="country")

        # appending ...
        location_interpretations.append(location_statistics)
    

    result = {
        "user":user_interpretaions,
        "location":location_interpretations
    }


    return Response(generate_res({"msg": result}))



@api_view(["GET"])
def tranaction_deep_dive(request):
    """
    This view is responsible for giving an in-depth exploratory details of the user transactions

    TO BE REMOVED-----------><------
    """
    try:
        all_transactions = TransactionReadSerializer(instance = request.user.transactions.all(), many =True)


        transformers = DataTransformationEngine(all_transactions.data)

        result = transformers.transform_amount(deep=True)

        return Response(generate_res({"msg": result}))
    except Exception as e:
        return Response(generate_res(err={"msg":str(e)}))



# 
# 
#  CIRCLE ...

class CircleCRUDView(APIView):

    def get(self, request):
        """
        This method returns a list of all circles a user is in if id(circle id) request param isnt provided else it returns a circle information

        Request param:
            id?: int(circle id)
        """

        circle_id = request.query_params.get("id", None)
        if circle_id:

            # getting the circle
            circle = Circle.objects.filter(pk = circle_id)

            # if the circle does not exists
            if not circle.exists():
                return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
            
            # subsetting the circle queryset
            circle = circle[0]

            # checking user member validity
            is_member = circle.is_member(request.user)

            # if the auth user is not a member
            if not is_member:
                return Response(generate_res(err={"msg":"You are not a member of this circle"}), status=status.HTTP_403_FORBIDDEN)
            serializer = CircleListSerializer(instance = circle)
        else:
            serializer = CircleSerializer(instance = request.user.circles.all(), many = True)
            
        return Response(generate_res({"msg":serializer.data}))
    

    def post(self, request):
        """
        This view is responsible for creating the circle instance

        Request data:
            name: str(circle name)
            description?: text
        """
        
        serializer = CircleSerializer(data = request.data)
        if serializer.is_valid():

            circle_name = request.data.get("name", None)
            # checking if the current user already own a circle with the same name
            user_circles = request.user.circles.all()

            # checking
            if user_circles.filter(name = circle_name).exists():
                return Response(generate_res(err={"msg":f"You already created or belonged to a circle called {circle_name}"}), status=status.HTTP_403_FORBIDDEN)
            
            # creating the circle
            serializer.save()

            # getting the circle created
            circle = serializer.instance

            # adding auth user as circle member with owner role
            circle.update_member(request.user, role="OWNER")
            return Response(generate_res({"msg":"circle created"}))
        return Response(generate_res(err={"msg":serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request):
        """
        This method is for updating the name and description of a circle and only the admin circle member is authorized to perform this operation

        Request param:
            id(int): circle id

        Request data:
            name?: str
            description?:str
        
        """
        circle_id = request.query_params.get("id", None)
        if not circle_id:
            return Response(generate_res(err={"msg":"circle id must be provided"}), status=status.HTTP_400_BAD_REQUEST)
        
        circle = Circle.objects.filter(pk=circle_id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
        circle = circle[0]

        # verifying user authorization for this operation
        is_member = circle.is_member(user=request.user)
        is_permitted = circle.is_admin(user=request.user)

        # if the auth user is not a circle member
        if not is_member:
            return Response(generate_res(err={"msg":"You are not a member of this circle"}), status=status.HTTP_401_UNAUTHORIZED)
        # if the auth user is a member of the circle but not the circle owner
        if is_member and not is_permitted:
            return Response(generate_res(err={"msg":"You are not authorized to carry out this operation"}), status=status.HTTP_401_UNAUTHORIZED)

        # initializing serializer
        serializer = CircleSerializer(instance = circle, data = request.data, partial= True)

        # performing field validation
        if serializer.is_valid():
            serializer.save()
            return Response(generate_res({"msg":"circle updated  successfully"}))
        
        return Response(generate_res(err={"msg":serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        This method is for deleting the circle and only the owner of the circle is authorized to perform this operation

        Request param:
            id(int): circle id

        Request data:
            name?: str
            description?:str
        
        """
        circle_id = request.query_params.get("id", None)
        if not circle_id:
            return Response(generate_res(err={"msg":"circle id must be provided"}), status=status.HTTP_400_BAD_REQUEST)
        circle = Circle.objects.filter(pk=circle_id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        # verifying user authorization for this operation
        single_circle = circle[0]
        is_member = single_circle.is_member(user=request.user)
        is_owner = single_circle.verify_member_role(user = request.user, role="OWNER")

        # if the auth user is not a circle member
        if not is_member:
            return Response(generate_res(err={"msg":"You are not a member of this circle"}), status=status.HTTP_401_UNAUTHORIZED)
        
        # if the auth user is a member of the circle but not the circle owner
        elif is_member and not is_owner:
            return Response(generate_res(err={"msg":"You are not authorized to carry out this operation"}), status=status.HTTP_401_UNAUTHORIZED)
        else:
            circle.delete()
            return Response(generate_res({"msg":"circle deleted successfully"}))
        


@api_view(["PUT"])
def add_circle_member(request, id):
    """
    This view is responsible for adding or updating(role) cirlce member

    Request data:
        user(id):int
        role?: MEMBER | ADMIN
    """

    # getting the auth user
    auth_user = request.user
    try:
        # getting request data
        req_user = request.data.get("user", None)
        req_role = request.data.get("role", "MEMBER")

        # Making sure the role provided is valid
        if req_role not in ["MEMBER", "ADMIN"]:
            raise Exception("The role available are MEMBER & ADMIN")
        
        # making sure the user is provided
        if not req_user:
            raise Exception("user must be provided")
        
        circle = Circle.objects.filter(pk=id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}))
        circle = circle[0]

        # AUTHORIZATION

        # checking if auth user is an admi
        is_admin =  circle.is_admin(auth_user)

        # if not, terminate the operation
        if not is_admin:
            return Response(generate_res(err={"msg":"You are not authorized to perform this operation"}), status=status.HTTP_401_UNAUTHORIZED)

        # checking if the user to be added has the same id as the auth user
        if auth_user.pk == req_user:
            return Response(generate_res(err={"msg":"You cannot update your membership status"}), status=status.HTTP_403_FORBIDDEN)
        
        # main operation
        circle.update_member(**request.data)
        return Response(generate_res({"msg":"Circle members updated successfully"}))

    except Exception as e:
        return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["PUT"])
def remove_circle_member(request, id):
    """
    This view is responsible for adding cirlce member

    Request data:
        user(id):int
    """
    try:
        # validating the prescence of a user in the request data
        if not request.data.get("user"):
            raise Exception("user must be provided")
        
        circle = Circle.objects.filter(pk=id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
        circle = circle[0]

        # verifying auth user authorization
        is_admin = circle.is_admin(user = request.user)
        if not is_admin:
            return Response(generate_res(err={"msg":"You are not authorized to perform this operation"}), status=status.HTTP_401_UNAUTHORIZED)
        
        circle.remove_member(**request.data)
        return Response(generate_res({"msg":"Member removed successfully"}))

    except Exception as e:
        return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
   