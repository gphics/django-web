
from account.tasks import update_profile_task
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from utils.res import generate_res
from .serializers import  (CategorySerializer,TransactionReadSerializer,TransactionCreationSerializer, CircleListSerializer, CircleSerializer, ShallowTransactionReadSerializer, CircleInviteReadSerializer, CircleInviteCreationSerializer)
from rest_framework import status
from .models import Transaction, Category, Circle, CircleInvite
from rapidfuzz import process as text_processor
from utils import DataInterpretationEngine, DataTransformationEngine, TransactionFileProcesor
from .pagination import TransactionPagination
from .filters import TransactionFilter
from utils.generate_clean_list import get_clean_list
from rest_framework.parsers import MultiPartParser, JSONParser,  FormParser
from rest_framework import serializers as MainSerializer
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Min, Max
from datetime import date
import pandas as pd
from ml import AnomalyDetectionEngine


# dd = ["a", "b"]
# if "a" not in dd:
#     print(1)
# else:
#     print(0)
# first = ShallowTransactionReadSerializer(many = True, instance = Transaction.objects.all())
# # second = DataTransformationEngine(first.data)
# df = pd.DataFrame(first.data)
# cols = ["amount", "category", "transaction_type", "transaction_date", "description"]

# new_df = df[cols].copy()
# # print(new_df.head())
# new_df.to_csv("bulk_transaction.csv", index=False)

# CATEGORY...
class CategoryCRUDView(APIView):
    """
    # This is the category CRUD class based view.
    """

    def get(self, request):
        """
        # This route retrieves all categories if title query param is not provided

        ## Request Query Param:
            > title?:string

        ## Return: List of categories or empty list
        """

        title = request.query_params.get("title", None)
   
        if title:
            serializer = CategorySerializer(instance = Category.objects.filter(title__icontains = title)[:5], many = True)
        else:
            serializer = CategorySerializer(instance = Category.objects.all()[:5], many = True)
        return Response(generate_res({"msg": serializer.data}))
       
       
    def post(self, request):
        """
        # This is the creation view for the category model.

        ## Request data:
            * title:str

        ## Return:
            * success message.
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


#  TRANSACTIONS ...
class TransactionCRUDView(APIView):
    """
    This class based view uses two serializers; one for creation and the other one for reading. I could have used one serializer but because I have two model fields that I wanna populate and might want to update and this would require tweeking and all sorts . so in order to make my code cleaner and easy to understand, I separated the logic.
    """

    parser_classes = [JSONParser , MultiPartParser, FormParser]
    
    def get(self, request):
        """
        # This view is responsible for retrieving user transactions

        ## Request Query:
            * id?:int --> transaction id

            * filtering params?:
                + flagged: bool (True| False)
                + transaction_type: (DEBIT | CREDIT)
                + category: title(str)
                + min_amount:int
                + max_amount:int
                + min_year: int
                + max_year: int
                + min_month: int
                + max_month: int
            
            ### Note: only one of the two query params can be present
        ## Return:
            + If id, transaction with the id is returned 
            + Else if any filtering parameter is provided, it returns the filtered data else all user transactions.
        """
        transaction_id = request.query_params.get("id", None)
        
        try:
            if transaction_id:
               
                #getting only one transaction
                trans = Transaction.objects.filter(pk = transaction_id)
                if not trans.exists():
                    raise Exception("Transaction does not exist")
                
                trans = trans[0]

                # If unauthorized access detected
                if trans.user != request.user:
                    return Response(generate_res(err={"msg":"Unauthorized accesss"}), status=status.HTTP_401_UNAUTHORIZED)
                
                # serializing the transaction data
                serializer = ShallowTransactionReadSerializer(instance = trans)
                
                return Response(generate_res({"msg":serializer.data}))
            else:

                # getting all user transactions
                queryset = Transaction.objects.filter(user = request.user)

                # verifying if user have transactions
                if queryset.count() < 1:
                    return Response(generate_res({"msg": "You have no transaction"}))

                # getting the url query params
                url_queries = {**request.query_params}

                # removing page if present
                url_queries.pop("page")

                for key, value in url_queries.items():
                    url_queries[key] = int(value[0]) if value[0].isdigit() else value[0]

                print(url_queries)
                # initializing the filterset
                filterset = TransactionFilter(url_queries, queryset=queryset )

                # checking if the filterset is valid
                if not filterset.is_valid():
                    return Response(generate_res(err={"msg":filterset.errors}), status=status.HTTP_400_BAD_REQUEST)
                
                # Resolving the queryset
                transactions = filterset.qs

                # If no matching transaction is found
                if not transactions.exists():
                    return Response( generate_res(err={"message": "No data found matching these filters."}), status=status.HTTP_404_NOT_FOUND )
               
                # initialising paginator
                paginator = TransactionPagination()

                # setting the total volume of transactions per page
                paginator.page_size=15

                # paginating the data
                results_page = paginator.paginate_queryset(transactions, request)

                # serializing the data
                serializer = ShallowTransactionReadSerializer(results_page, many=True)

                return paginator.get_paginated_response(serializer.data)
              
            
        except Exception as e:
            return Response(generate_res(err={"msg": str(e)}), status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        
        """
        # This view is responsible for creating transactions

        ## Request data:
            -  amount: int
            -  category: category id(int) | title(str)
            -  transaction_date?: datetime(str)
            -  transaction_file?: a csv file. for multiple transactions upload.
       
        ## Return:
            - success message if no error.


        """

        # getting transaction file
        transaction_file = request.data.get("transaction_file", None)
        # IF FILE 
        if transaction_file:
            try:
               
                file_processor = TransactionFileProcesor(transaction_file)

                # getting the processed data from the file
                processed_data:list = file_processor.transform_to_json()

                # initializing atomic pattern to allow for rollback if an error occurs during this large operation
                with transaction.atomic():

                    # looping through ...
                    for data in processed_data:

                        # initializing serializer
                        data_serializer = TransactionCreationSerializer(data={**data, "user": request.user.pk}, context={"request":request})

                        # validating the data
                        if data_serializer.is_valid():

                            # saving the transactions
                            data_serializer.save()

                        # if an error occured in the serializer
                        else:
                            return Response(generate_res(err={"msg":data_serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
                
                # if no error occurs
                return Response(generate_res({"msg":f"All {len(processed_data)} transactions created successfully. "}))
                
            # this is responsible for catching the exceptions that originate from the TransactionFileProcessor
            except Exception as e:
                print(e)
                return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
            


        # IF JSON DATA
        try:
            serializer = TransactionCreationSerializer(data={**request.data, "user":request.user.pk}, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response(generate_res({"msg":"transaction created"}))

            # catching the error if the required data is missing
            return Response(generate_res(err={"msg":serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
           
        # Additional error catching layer
        except MainSerializer.ValidationError as e:
            return Response(generate_res(err={"msg":e.detail}), status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request):
        """
        # This view is for updating the transaction object.

        ## Request query:
            * id:int -> transaction id
        ## Return:
            * success message if no error
        """
        try:
            transaction_id = request.query_params.get("id", None)

            # getting the transaction instance
            trans = Transaction.objects.filter(pk = int(transaction_id))
            if not trans.exists():
                return Response(generate_res(err={"msg": "transaction does not exist"}), status=status.HTTP_404_NOT_FOUND)
            serializer = TransactionCreationSerializer(instance = trans[0], data = request.data,context={"request":request}, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(generate_res({"msg":"transaction updated"}))
            
          

            # updating the user profile in the background
            update_profile_task.delay_on_commit(trans[0].user.pk)

            # returning status message ...
            return Response(generate_res(err={"msg": serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(generate_res(err={"msg": str(e)}), status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        """
        # This view is for deleting the transaction.

        ## Request param:
            id : transaction id(int)

        ## Return:
            + success message if no error.


        """
        transaction_id = request.query_params.get("id", None)
        trans = Transaction.objects.filter(pk = transaction_id)
        if not trans.exists():
             return Response(generate_res(err={"msg": "transaction does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        trans.delete()
        return Response(generate_res({"msg":"transaction deleted"}))
    

@api_view(["GET"])
def detect_anomaly(request):
    user_transactions = request.user.transactions.all()
    serializer = ShallowTransactionReadSerializer(user_transactions ,many = True)

    transformer = DataTransformationEngine(serializer.data)

    model = AnomalyDetectionEngine(transformer.get_df_copy_to_list())

    model.train_model()

    predictions = model.predict()

    anomalous_transaction_count = 0

    with transaction.atomic():
        for pred in predictions:
            flagged = pred["flagged"]
            pred_id = pred["id"]
            trans = Transaction.objects.get(id = pred_id)
            trans.flagged = flagged
            trans.save()

            if flagged:
                anomalous_transaction_count +=1
    resultStr = "No anomalous transaction detected." if anomalous_transaction_count == 0 else f"{anomalous_transaction_count} anomalous transaction(s) detected."
    return Response(generate_res({"msg":{
        "is_anomalous": bool(anomalous_transaction_count),
        "resultStr":resultStr
    }}))
# 
# 
# HELPER FUNCTIONS THAT I DELIBERATELY PLACED HERE BECAUSE THEY USE CERTAIN INFORMATION IN THIS MODULE
# WHICH IS QUITE DIFFICULT TO MOVE AROUND

def helper_for_interpret(location_type:str, location:str, currency:str, financial_activity:str, user_transactions_count:int, req_filters:dict) -> list:
    """
    This function is helping the interpret_summary_statistics view

    Returns:
        [location_statistics:dict, transformer:obj]
    """

    # filtering base on location and it's type
    filters = {location_type: location}
    location_transactions = Transaction.objects.filter(**filters)

    # Guarding this ops so that it is only performed when all the transactions in the location does not belong to the auth user alone
    if location_transactions.count() == user_transactions_count:
        return "Operation not suitable to perform"
    
    # Initialising filterset for advanced filtering / sorting
    filterset = TransactionFilter(req_filters, queryset=location_transactions)

    if not filterset.is_valid():
        return str(filterset.errors)
    
    location_transactions = filterset.qs

    # if the filtered data is less than 2, then the following operation is not worth doing, hence I am terminating the function
    if location_transactions.count() < 2:
        return "Operation not suitable to perform"

    # serializing the data
    location_serializer = ShallowTransactionReadSerializer(instance =location_transactions , many = True)

    # initialising the data transformer
    transformer = DataTransformationEngine(location_serializer.data)

    

    # calculating the location summary statistics
    json_data = {"amount":transformer.transform_amount()}

    # initialising summary statistics interpreter
    interpreter = DataInterpretationEngine(json_data, currency=currency, financial_activity=financial_activity)

    # interpreting the summary statistics
    location_statistics = interpreter.interpret_location_amount(location, location_type)
    
    # the amount data:Series for the location
    location_amount = transformer.get_raw_transaction_amount(n=user_transactions_count)
     
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
        paragraph = f""" The data shows a significant difference between your financial activity and others in your {location_type}. You’re trending {spending_step_str} than the typical user in a way that really counts. """
    else:
        paragraph = f""" Your financial activity is right in line with others in your {location_type}. There's no significant difference between your habits and the local average. """

    return paragraph

@api_view(["GET"])
def interpret_summary_statistics(request):
    """
    # This view is responsible for interpreting the summary statistics.
        Including:
            + amount
            + amount(deep)
            + transaction_date
        For users and his/her location.

    ## It also support filtering that is applied to the user and locations of transactions.

       * filtering params?:
                    + flagged: bool (True| False)
                    + transaction_type: (DEBIT | CREDIT)
                    + category: title(str)
                    + min_amount:int
                    + max_amount:int
                    + min_year: int
                    + max_year: int
                    + min_month: int
                    + max_month: int

    ## Return:
        * Interpreted information gotten from the data
        
    """

    # 
    # 
    # WORKING ON USER INTERPRETATIONS

    # getting all user transactions
    user_transactions =request.user.transactions.all()

    # checking the number of user transactions
    user_transaction_count = user_transactions.count()
    if user_transaction_count  < 2:
        return Response(generate_res(err={"msg":"Add more transactions to perform this operation"}), status=status.HTTP_400_BAD_REQUEST)

    filterset = TransactionFilter(request.query_params, queryset=user_transactions)

    if not filterset.is_valid():
        return Response(generate_res(err={"msg":filterset.errors}), status=status.HTTP_400_BAD_REQUEST)
    
    user_transactions = filterset.qs


      # checking the number of user transactions
    user_transaction_count = user_transactions.count()
    if user_transaction_count  < 2:
        return Response(generate_res(err={"msg":"You have no transactions that match the filter"}), status=status.HTTP_400_BAD_REQUEST)

    # serializing the user transactions
    all_transactions = ShallowTransactionReadSerializer(instance = user_transactions, many = True)
    

    transformer = DataTransformationEngine(all_transactions.data)
   
   

    # json data of the summary_statistics
    json_data = {
        "amount": transformer.transform_amount(),
        "transaction_dates": transformer.transform_transaction_date(),
        "amount_by_date": transformer.transform_amount(deep=True),
        "category": transformer.basic_transformation("category"),
        "flagged": transformer.basic_transformation("flagged"),
        "transaction_type": transformer.basic_transformation("transaction_type"),
    }
    interpreter = DataInterpretationEngine(json_data, currency=request.user.profile.currency, financial_activity=request.user.profile.financial_activity)

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
    financial_activity =request.user.profile.financial_activity  

    # Handling location statistics
    
    # Guarding this ops so that it is only performed when all the transactions in the location does not belong to the auth user alone

    city_result = helper_for_interpret("city", city, currency, financial_activity, user_transaction_count, req_filters=request.query_params)
    state_result = helper_for_interpret("state", state, currency, financial_activity, user_transaction_count, req_filters=request.query_params)
    country_result = helper_for_interpret("country", country, currency, financial_activity, user_transaction_count, req_filters=request.query_params)

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
        "location":get_clean_list(location_interpretations),
        "comparisons":get_clean_list([city_comparison, state_comparison, country_comparison])
    }

    
  

    return Response(generate_res({"msg": result}))


# 
# 
#  CIRCLE ...

class CircleCRUDView(APIView):

    def get(self, request):
        """
        # This method returns a list of all circles a user is in, if id(circle id) request param isn't provided else it returns a circle information

        ## Request param:
            - id?: int(circle id)

        ## Return: 
            - Circle(s) if no error
        """

        # getting circle id
        circle_id = request.query_params.get("id", None)

        # getting only one circle
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
            
            # initializing circle serializer
            serializer = CircleListSerializer(instance = circle)
        else:
            serializer = CircleSerializer(instance = request.user.circles.all(), many = True)
            
        return Response(generate_res({"msg":serializer.data}))
    

    def post(self, request):
        """
        # This view is responsible for creating the circle.

        ## Request data:
            + name: str(circle name)
            + description?: text

        ## Return:  
            + success message if no error
        """
        
        serializer = CircleSerializer(data = request.data)
        if serializer.is_valid():

            circle_name = request.data.get("name", None)
            # checking if the current user already own a circle with the same name
            user_circles = request.user.circles.all()

            # checking...
            if user_circles.filter(name = circle_name).exists():
                return Response(generate_res(err={"msg":f"You already belonged to this circle"}), status=status.HTTP_403_FORBIDDEN)
            
            # creating the circle
            serializer.save()

            # getting the circle created
            circle = serializer.instance

            # adding auth user as circle member with owner role
            circle.update_member(request.user, role="OWNER")
            return Response(generate_res({"msg":"circle created"}))
        
        # handling serializer errors
        return Response(generate_res(err={"msg":serializer.errors}), status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request):
        """
        # This method is for updating the name and description of a circle.
         
        ## Authorization:
            - Circle admin only

        ## Request query:
            - id(int): circle id

        ## Request data:
            - name?: str
            - description?:str

        ## Return:
            - success message if no error
        
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
        #This method is for deleting the circle.

        ## Authorization:
            - Circle owner only

        ## Request query:
            - id(int): circle id

        ## Return:
            - success message if no error
        
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
        
 
class CircleInvitationCRUDView(APIView):

    def get(self, request):

        """
        ## This route is responsible for reading all user invitations.

        ### Returns: list()
        """
        invitations = request.user.invitations.all()
        serializer = CircleInviteReadSerializer(many = True, instance = invitations)
        return Response(generate_res({"msg": serializer.data}))

    def post(self, request):
        """
        ## This route is responsible for creating circle invite

        ### Request data:
            > circle(id):int
            > user(recipient id):int

        ## NOTE: Only circle admin(ADMIN | OWNER) are authorized to do this
        """
        
        auth_user = request.user

        # request data
        circle_id = request.data.get("circle", None)
        recipient_user_id = request.data.get("user", None)

        if not circle_id or not recipient_user_id:
            return Response(generate_res(err={"msg": "Required data must be provided"}), status=status.HTTP_400_BAD_REQUEST)
        
        circle = Circle.objects.filter(id=circle_id)
        if not circle.exists():
            return Response(generate_res(err={"msg": "Circle does not exists"}), status=status.HTTP_404_NOT_FOUND)
        circle = circle[0]

        # verifying authorization (ADMIN | MEMBER) for auth user
        is_auth_user_permitted = circle.is_admin(auth_user)
        if not is_auth_user_permitted:
            return Response(generate_res(err={"msg": "Unauthorized action"}), status=status.HTTP_401_UNAUTHORIZED)
        
        
        # fetching the recipient user data
        recipient_user = User.objects.filter(id = recipient_user_id)
        if not recipient_user.exists():
            return Response(generate_res(err={"msg": "Recipient user does not exists"}), status=status.HTTP_404_NOT_FOUND)
        recipient_user = recipient_user[0]

        # checking if recipient user is already a member
        is_recipient_already_a_member = circle.is_member(recipient_user)

        if is_recipient_already_a_member:
            return Response(generate_res(err={"msg": "Recipient user is already a member"}), status=status.HTTP_400_BAD_REQUEST)
        
        # creating invite
        serializer = CircleInviteCreationSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(generate_res({"msg":"Invitation sent"}))
        return Response(generate_res(err={"msg": serializer.errors}), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        ## This route is responsible for accepting or declining circle invitations

        ## Request data:
            > id (invitation id):int
            > status (ACCEPTED | DECLINED)

        """
        # request data

        invitation_id:int = request.data.get("id", None)
        invitation__status:str = request.data.get("status", None)

        acceptable_status_list = ["ACCEPTED", "DECLINED"]

        # validating the request data
        if not invitation_id:
            return Response(generate_res(err={"msg": "invitation id must be provided"}), status=status.HTTP_400_BAD_REQUEST)
        
        if invitation__status not in acceptable_status_list:
            return Response(generate_res(err={"msg": "invalid invitation status provided"}), status=status.HTTP_400_BAD_REQUEST)
        
        # fetching invitation
        invitations = CircleInvite.objects.filter(id = invitation_id)
        if not invitations.exists():
            return Response(generate_res(err={"msg": "invitation does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        # subsetting the invitation
        invitation = invitations[0]
    
        # condition for accepting invitation
        response_text ="invitation declined"
        if invitation__status == acceptable_status_list[0]:
            recipient_user = invitation.user
            circle = invitation.circle

            # adding member
            circle.update_member(user = recipient_user)
            circle.save()
            response_text ="invitation accepted"
        
        # deleting invitation because it is no longer needed
        invitation.delete()

        return Response(generate_res(err={"msg": response_text}))
        

    # 
    # 
    # LEGACY ...
    # 
    # 

    def delete(self, request):
        """
        ## This route is responsible for deleting invitations after it's "is_accepted" status changes

        ### Request query:
            > id(invitation id):int
        """
        invitation_id = request.query_params("id", None)
        if not invitation_id:
            return Response(generate_res(err={"msg": "invitation id must be provided"}), status=status.HTTP_400_BAD_REQUEST)
        
        invitations = CircleInvite.objects.filter(id = invitation_id)
        if not invitations.exists():
            return Response(generate_res(err={"msg": "invitation does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        invitations.delete()
        return Response(generate_res({"msg": "invitation deleted successfully"}))


#
#
# LEGACY ...
#
#
@api_view(["PUT"])
def add_circle_member(request, id:int):
    """
    # This view is responsible for adding or updating(role) circle member

    ## Request Param:
        * id:int -> circle id

    ## Request data:
        * user(id):int
        * role?: MEMBER | ADMIN

    ## Return:
        * success message if no error
    """

    # getting the auth user
    auth_user = request.user
    try:
        # getting request data
        req_user_id = request.data.get("user", None)
        req_role = request.data.get("role", "MEMBER")

        # Making sure the role provided is valid
        if req_role not in ["MEMBER", "ADMIN"]:
            raise Exception("The roles available are MEMBER & ADMIN")
        
        # making sure the user is provided
        if not req_user_id:
            raise Exception("user id must be provided")
        
        # getting the req user User instance
        req_user = User.objects.filter(pk = req_user_id)
        if not req_user.exists():
            raise Exception("User to be added to the circle does not exist")
        
        # subsetting req_user
        req_user = req_user[0]
        
        circle = Circle.objects.filter(pk=id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}))
        circle = circle[0]

        # AUTHORIZATION

        # checking if auth user is an admin
        is_admin =  circle.is_admin(auth_user)

        # if not, terminate the operation
        if not is_admin:
            return Response(generate_res(err={"msg":"You are not authorized to perform this operation"}), status=status.HTTP_401_UNAUTHORIZED)

        # checking if the user to be added has the same id as the auth user
        if auth_user.pk == req_user_id:
            return Response(generate_res(err={"msg":"You cannot update your membership status"}), status=status.HTTP_403_FORBIDDEN)
        
        
        # main operation
        circle.update_member(role=req_role, user=req_user)
        return Response(generate_res({"msg":"Circle members updated successfully"}))

    except Exception as e:
        return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["DELETE"])
def remove_circle_member(request, id):
    """
    # This view is responsible for removing circle member by the circle admin

    ## Request param:
        + id:int -> circle id

    ## Request query:
        + user:int -> circle member user id
    
    ## Return:
        + success message if no error

    """
    try:
        req_user_id = request.query_params.get("user", None)
        # validating the prescence of a user in the request data
        if not req_user_id:
            raise Exception("user must be provided")
        
         # getting the req user User instance
        req_user = User.objects.filter(pk = req_user_id)
        if not req_user.exists():
            raise Exception("User to be added to the circle does not exist")
        
        # subsetting req_user
        req_user = req_user[0]

        
        
        circle = Circle.objects.filter(pk=id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        # subsetting circle queryset
        circle = circle[0]

        # checking if req user is a member of the circle
        is_member = circle.is_member(req_user)

        # if req user is not a circle member
        if not is_member:
            return Response(generate_res(err={"msg":"User is not a member of this circle"}), status=status.HTTP_404_NOT_FOUND)
        

        # verifying auth user authorization
        is_admin = circle.is_admin(user = request.user)
        if not is_admin:
            return Response(generate_res(err={"msg":"You are not authorized to perform this operation"}), status=status.HTTP_401_UNAUTHORIZED)
        
        circle.remove_member(user=req_user)
        return Response(generate_res({"msg":"Member removed successfully"}))

    except Exception as e:
        return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
   

@api_view(["DELETE"])
def leave_circle(request, id:int):

    """
    # This view is for autheticated user who is a circle member to leave the circle.

    ## Request param:
        * id:int -> circle id

    ## Return:
        * success message if no error
    """

    try:
        circle = Circle.objects.filter(pk=id)
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        # subsetting circle queryset
        circle = circle[0]

        auth_user = request.user

        # checking if auth user is a member of the circle
        is_member = circle.is_member(auth_user)

        # if auth user is not a circle member
        if not is_member:
            return Response(generate_res(err={"msg":"You are not a member of this circle"}), status=status.HTTP_401_UNAUTHORIZED)
        
        # checking if the auth user is the owner of the circle
        is_owner = circle.verify_member_role(user=auth_user, role="OWNER")

        # if true
        if is_owner:
            return Response(generate_res(err={"msg":"You cannot leave the circle but you can delete it."}), status=status.HTTP_401_UNAUTHORIZED)
        
        # removing auth user from the circle
        circle.remove_member(auth_user)

        return Response(generate_res({"msg":"You left the circle"}))
    except Exception as e:
        return Response(generate_res(err={"msg":str(e)}), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def rank_circle_members(request, id:int):
    """
    # This view is resposible for ranking the circle members base on a specific summary statistics paramter with the default beign mean transaction amount.

    ## Request query:
        - stat?:str -> [mean(default), min, max, count, std] 

    ## Return:
        - a sorted list of circle members
    """
    try:
        # getting the stat query param
        stat_param = request.query_params.get("stat", "mean")

        # getting the circle instance
        circle = Circle.objects.filter(pk = id)
        

        # if the circle instance exist
        if not circle.exists():
            return Response(generate_res(err={"msg":"circle does not exist"}), status=status.HTTP_404_NOT_FOUND)
        
        # subsetting circle
        circle = circle[0]

        # verifying if auth user is a member
        if not circle.is_member(request.user):
            return Response(generate_res(err={"msg":"You are not a member of this circle"}), status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CircleListSerializer(instance = circle)
        # sorting the circle members
        result = serializer.sort_by(data=serializer.data["members"], summ_stat_param=stat_param)

        return Response(generate_res({"msg": result}))
    except Exception as e:
        return Response(generate_res(err={"msg": str(e)}), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def get_filtering_limit(request):
    """
    # This route is responsible for getting the filtering limits for each user.
    
    ## Result
        * filtering params?:
                    + flagged: bool (True| False)
                    + transaction_type: (DEBIT | CREDIT)
                    + category: title(str)
                    + min_amount:int
                    + max_amount:int
                    + min_year: int
                    + max_year: int
                    + min_month: int
                    + max_month: int
    """

    user_transactions = Transaction.objects.filter(user = request.user)
    today = date.today()
    # dates
    combinations = user_transactions.aggregate(min_year = Min("transaction_date__year") or today.year , max_year=Max("transaction_date__year") or today.year, min_amount=Min("amount") or 0, max_amount=Max("amount") or 1000)

    # months = user_transactions.values_list("transaction_date__month", flat=True).order_by().distinct()

    categories = user_transactions.values_list("category__title", flat=True).order_by("category__title").distinct()

    result = {
        "flagged": [True, False],
        "transaction_type": ["DEBIT", "CREDIT"],
        "categories":categories,
        **combinations,
    }
    return Response(generate_res({"msg": result}))