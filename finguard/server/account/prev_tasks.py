from transaction.serializers import ShallowTransactionReadSerializer
from transaction.models import Transaction
from .models import Profile
from utils import DataTransformationEngine, get_financial_activity
from django.db import transaction
from celery.utils.log import get_task_logger
from celery import shared_task

# 
# 
# LEGACY
# 
# 
# 

logger = get_task_logger(__name__)

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
            
def process_summary_stat(user_id:int):
    """
    This function updat the user profile with the summary statistics
    """

    # getting user profile
    user_profile = Profile.objects.get(user = user_id)

    # getting the total transaction count
    user_transaction_count = user_profile.user.transactions.all().count()
   
    # if the number of user transactions is less than 2
    if user_transaction_count < 2 :

        # setting summary statistics to null
        user_profile.summary_statistics = None

        # saving the update
        user_profile.save()

      # terminating early ...
        return
    
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

@shared_task
def update_profile_task(user_id:int):
    process_summary_stat(user_id)
    logger.info("Profile summary statistics updated")