from django.dispatch import receiver
from .models import Transaction
from account.models import Profile
from django.db.models.signals import post_save, post_delete
from .tasks import handle_transaction_post_save
from .serializers import ShallowTransactionReadSerializer
from utils import DataTransformationEngine, get_financial_activity
import traceback
from django.db import transaction
from ml import AnomalyDetectionEngine

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
    
def ml_action(instance, retrain=False):
    """
    # What data to send:
        - For retrain, I send all user transactions
        - For user transaction count equals 5, I also send all user transactions. (First model creation)
        - Else (not retrain and user transaction count is >5), send the instance data.

    # Conditions for a retrain:
        - First model creation: the retrain serves as a guide so that the new model can be saved locally. Just for direction.

        - Actual retrain
        
    """
    # if the ml model is currently beign retrained,
    # then terminate early.

    if instance.user.profile.is_ml_model_busy:
        return
    
    # else, continue

    user_transactions = instance.user.transactions.all()
    user_transaction_count = user_transactions.count()

    if retrain or user_transaction_count == 5:
        serializer = ShallowTransactionReadSerializer(instance = user_transactions, many=True)
    else:
        serializer = ShallowTransactionReadSerializer(instance = [instance], many=True)

    # initialising the data transformation engine
    transformer = DataTransformationEngine(serializer.data)

    # initializing the model
    model = AnomalyDetectionEngine(data = transformer.get_df_copy_to_list(["flagged"]), user_id=instance.user.pk, retrain=retrain)
    
    model.train_model() 

    predictions = model.predict()

    # updating the transaction(s)
    # using atomic to enable db rollback with absolute integrity

    with transaction.atomic():

        # looping through the predictions
        for pred in predictions:
            # destructuring each prediction
            flagged = pred.get("flagged")
            id_ = pred.get("id")

            # fetching the matching transactionnn
            single_transaction = Transaction.objects.get(pk = id_)

            # updating flagged
            single_transaction.flagged = flagged

            # saving the updated transaction
            single_transaction.save()
            
    
def main_action(instance):
    """
    This function encapsulates all operations needed to be carried out when a transaction is created, updated or deleted

    Field Updated:
        summary_statistics
        number_of_transactions
        spending_pattern

    """

    user_profile = instance.user.profile
    
    user_transaction_count = instance.user.transactions.all().count()

    # 
    # MODELLING
    # 
    # RULES:
    # The ml operation is only performed when 
    #   user transactions is >= 5
    if user_transaction_count >= 5:
        ml_action(instance)

    
    # 
    # SUMMARY STATISTICS
    # if the number of user transactions is less than 2
    if user_transaction_count < 2:

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

        with transaction.atomic():

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
 
    # making sure the action is done only when a transaction is created
    if created:
        handle_transaction_post_save(main_action, instance)
        
           

@receiver(post_delete, sender=Transaction)
def second_update_profile(sender, instance, **kwargs):
    """
    This signal fires when a transactions is deleted
    """

    # calling the background task
    handle_transaction_post_save.delay(main_action, instance)