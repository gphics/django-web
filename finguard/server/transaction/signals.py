from django.dispatch import receiver
from .models import Transaction
from account.models import Profile
from django.db.models.signals import post_save, post_delete

from .serializers import ShallowTransactionReadSerializer
from utils import DataTransformationEngine, get_financial_activity
import traceback
from django.db import transaction

def get_summary_stat(user):
    """
    This function get a shallow summary statistics for the amount feature
    """
    # getting user transactions queryset
    all_transactions = user.transactions.all()

    # serializing the all_transactions queryset to python data type
    serializer = ShallowTransactionReadSerializer(instance = all_transactions, many = True)

    
    # getting serialized transactions
    all_transactions = serializer.data

    # initialising the data transformation engine

    transformer = DataTransformationEngine(all_transactions)

    amount_summary_stat = transformer.transform_amount()
    
    
    # returning the amount summary statistics
    return amount_summary_stat
    
    
    
def main_action(instance):
    """
    This function encapsulates all operations needed to be carried out when a transaction is created, updated or deleted

    Field Updated:
        summary_statistics
        number_of_transactions
        spending_pattern

    """

    user_profile = Profile.objects.filter(user = instance.user)

    # checking if user profile exist
    if not user_profile.exists():
        raise Exception("User profile does not exist")
    

    user_profile = user_profile[0]
        
    # if the number of user transactions is less than 2
    if len(list(user_profile.user.transactions.all())) < 2:

        # setting summary statistics to null
        user_profile.summary_statistics = None

        # saving the update
        user_profile.save()

        # terminating early ...
        return
    #  if the number of user transactions is greater than 2
    try:
        # calculating summary stat
        result = get_summary_stat(user_profile.user)

        # getting the params needed by theget_spending_pattern function
        std = result["std"]
        mean = result["mean"]
        count = abs(result["count"])

        with  transaction.atomic():

            # updating number of transactions
            user_profile.number_of_transactions = count

            # updating spending pattern
            user_profile.financial_activity = get_financial_activity(std, mean)

            # updating profile summary statistics
            user_profile.summary_statistics = result 

            # saving the update
            user_profile.save()

    except Exception as e:
        traceback.print_exc()


@receiver(post_save, sender=Transaction)
def update_profile(sender, instance, created, **kwargs):
    """
    This signal fires when an update or create action is taken on the Transaction model
    """
    main_action(instance)
           

@receiver(post_delete, sender=Transaction)
def second_update_profile(sender, instance, **kwargs):
    """
    This signal fires when a transactions is deleted
    """
    main_action(instance)