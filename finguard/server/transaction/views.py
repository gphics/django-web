from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from utils.res import generate_res
from .serializers import  (CategorySerializer,TransactionReadSerializer,TransactionCreationSerializer, CircleListSerializer, CircleSerializer, ShallowTransactionReadSerializer)
from rest_framework import status
from .models import Transaction, Category, Circle
from rapidfuzz import process as text_processor
from utils import DataInterpretationEngine, DataTransformationEngine

# Create your views here.
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

        serializer = TransactionCreationSerializer(data={**request.data, "user":request.user.pk}, context={"request": request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(generate_res({"msg":"transaction created"}))
        else:
            return Response(generate_res(err={"msg":serializer.errors}), status=status.HTTP_404_NOT_FOUND)
       
       
        
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
    
# 
# 
# HELPER FUNCTIONS THAT I DELIBERATELY PLACED HERE BECAUSE THEY USE CERTAIN INFORMATION IN THIS MODULE
# WHICH IS QUITE DIFFICULT TO MOVE AROUND

def helper_for_interpret(location_type:str, location:str, currency:str, spending_pattern:str, user_transactions_count) -> list:
    """
    This function is helping the interpret_summary_statistics view

    Returns:
        [location_statistics:dict, transformer:obj]
    """

    filters = {location_type: location}
    location_transaction = Transaction.objects.filter(**filters)

    # Guarding this ops so that it is only performed when all the transactions in the location does not belong to the auth user alone
    if location_transaction.count() == user_transactions_count:
        return "Operation not suitable to perform"

    # serializing the data
    location_serializer = ShallowTransactionReadSerializer(instance =location_transaction , many = True)

    # initialising the data transformer
    transformer = DataTransformationEngine(location_serializer.data)

    

    # calculating the location summary statistics
    json_data = {"amount":transformer.transform_amount()}

    # initialising summary statistics interpreter
    interpreter = DataInterpretationEngine(json_data, currency=currency, spending_pattern=spending_pattern)

    # interpreting the summary statistics
    location_statistics = interpreter.interpret_location_amount(location, location_type)
    
    # the amount data:Series for the location
    location_amount = transformer.get_raw_transaction_amount()
    
     # the amount data mean for the location
    location_amount_mean = transformer.get_transaction_amount_mean()

    return [location_statistics, [location_amount, location_amount_mean]]


def handle_comparisons(location_amount, location_amount_mean:float, user_transformer:DataTransformationEngine, location_type="city") -> str :
    """
    This function compute and determine the statistical difference of a user against the provided location if all the transactions in the location does not belong to the user alone
    """

    significance_state = user_transformer.check_mean_significance_ind(location_amount)

    user_amount_mean = user_transformer.get_transaction_amount_mean()

    spending_step_str = "lower" if user_amount_mean < location_amount_mean else "higher"

    # interpreting the result
    if significance_state:
        paragraph = f""" The data shows a significant difference between your spending and others in your {location_type}. You’re trending {spending_step_str} than the typical user in a way that really counts. """
    else:
        paragraph = f""" Your spending is right in line with others in your {location_type}. There's no significant difference between your habits and the local average. """

    return paragraph

@api_view(["GET"])
def interpret_summary_statistics(request):
    """
    This view is responsible for interpreting the summary statistics.
    Including:
        amount
        amount(deep)
        transaction_date

    Lastly, this function split transactions base on user location data 
        
    """

    # 
    # 
    # WORKING ON USER INTERPRETATIONS

    # getting all user transactions
    user_transactions =request.user.transactions.all()
    user_transaction_count = user_transactions.count()
    if user_transaction_count  < 2:
        return Response(generate_res(err={"msg":"Add more transactions to perform this operation"}), status=status.HTTP_400_BAD_REQUEST)
    
    # serializing the user transactions
    all_transactions = ShallowTransactionReadSerializer(instance = user_transactions, many = True)


    transformer = DataTransformationEngine(all_transactions.data)


    # json data of the summary_statistics
    json_data = {
        "amount": transformer.transform_amount(),
        "transaction_dates": transformer.transform_transaction_date(),
        "amount_by_date": transformer.transform_amount(deep=True),
        "category": transformer.basic_transformation("category"),
        "transaction_type": transformer.basic_transformation("transaction_type"),
    }
    interpreter = DataInterpretationEngine(json_data, currency=request.user.profile.currency, spending_pattern=request.user.profile.spending_pattern)

    # interpreting all user related statistics
    user_interpretaions = interpreter.interpret_all()


    #
    #
    # WORKING ON LOCATION INTERPRETATIONS

    # getting auth user location data
    # A guard clause e.g (or None ) was not added because a user cannot create a transaction without having all profile location info
    city = request.user.profile.city  
    state = request.user.profile.state 
    country = request.user.profile.country
    currency =request.user.profile.currency
    spending_pattern =request.user.profile.spending_pattern  

    # Handling location statistics
    
    # Guarding this ops so that it is only performed when all the transactions in the location does not belong to the auth user alone

    city_result = helper_for_interpret("city", city, currency, spending_pattern, user_transaction_count)
    state_result = helper_for_interpret("state", state, currency, spending_pattern, user_transaction_count)
    country_result = helper_for_interpret("country", country, currency, spending_pattern, user_transaction_count)

    # checking if the location ops returns a string because all the transactions in the location belong to the auth user
    is_city_result:bool = not isinstance(city_result, str)
    is_state_result:bool = not isinstance(state_result, str)
    is_country_result:bool = not isinstance(country_result, str)

    # wrapping all the location stat into a list
    # adding the location result base on a condition

    location_interpretations = [
        is_city_result and city_result[0],
        is_state_result and state_result[0], 
        is_country_result and country_result[0]
        ]
    
    
    
    # comparing location average to user average
    # performing this operation conditionally
    city_comparison:bool | str  = is_city_result and handle_comparisons(*city_result[1], transformer, location_type="city")
    state_comparison:bool | str  = is_state_result and handle_comparisons(*state_result[1], transformer, location_type="state")
    country_comparison:bool | str  = is_country_result and handle_comparisons(*country_result[1], transformer, location_type="country")


    result = {
        "user":user_interpretaions,
        "location":location_interpretations,
        "comparisons":[city_comparison, state_comparison, country_comparison]
    }

    
  

    return Response(generate_res({"msg": result}))


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
   