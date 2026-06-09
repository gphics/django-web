# from transaction.models import Transaction
# from celery import shared_task
# from celery.utils.log import get_task_logger
# from .ml_engine import AnomalyDetectionEngine, ModelStorageEngine
# from django.db import transaction, close_old_connections
# from account.models import Profile
# from transaction.serializers import ShallowTransactionReadSerializer
# from utils import DataTransformationEngine
# from django.db import transaction
# from transaction.models import Transaction
# from ml.models import TransactionTrack

# logger = get_task_logger(__name__)

# def transaction_flagging_ml_process(instance_id, retrain=False):
#     """
#     # What data to send:
#         - For retrain, I send all user transactions
#         - For user transaction count equals 5, I also send all user transactions. (First model creation)
#         - Else (not retrain and user transaction count is >5), send the instance data.

#     Conditions for a retrain:
#         - First model creation: the retrain serves as a guide so that the new model can be saved locally. Just for direction.

#         - Actual retrain
        
#     """
 
#     # getting the transaction instance
#     instance = Transaction.objects.get(pk = instance_id)

#     # if the ml model is currently beign retrained,
#     # then terminate early.
#     if instance.user.profile.is_ml_model_busy:
#         return
    
#     # else, continue
#     user_transactions = instance.user.transactions.all()
#     user_transaction_count = user_transactions.count()

   

#     # RULES:
#     # The ml operation is only performed when 
#     #   user transactions is >= 5
#     if user_transaction_count < 5:
#         return

#     # else, continue
   
#     if retrain or user_transaction_count == 5:
#         serializer = ShallowTransactionReadSerializer(instance = user_transactions, many=True)
#     else:
#         serializer = ShallowTransactionReadSerializer(instance = [instance], many=True)

#     # initialising the data transformation engine
#     transformer = DataTransformationEngine(serializer.data)
 
#     # initializing the model
#     model = AnomalyDetectionEngine(data = transformer.get_df_copy_to_list(["flagged"]), user_id=instance.user.pk, retrain=retrain)
    
#     # updating transaction track ...
#     trans_track = TransactionTrack.objects.get(user = instance.user)
#     trans_track.previous_transaction_count = user_transaction_count

#     # saving ...
#     trans_track.save()
    
#     # training the model ...
#     model.train_model() 

#     # making the predictions ...
#     predictions = model.predict()

#     # updating the transaction(s)
#     # using atomic to enable db rollback with absolute integrity

#     with transaction.atomic():

#         # looping through the predictions
#         for pred in predictions:
#             # destructuring each prediction
#             flagged = pred.get("flagged")
#             id_ = pred.get("id")

#             # fetching the matching transactionnn
#             single_transaction = Transaction.objects.get(pk = id_)

#             # updating flagged
#             single_transaction.flagged = flagged

#             # saving the updated transaction
#             single_transaction.save()

# @shared_task(bind=True, max_retries=2)
# def flag_transactions(self, instance_id:int):
#     """
#     # This background function get called when a transaction is created or updated

#     ## Params:
#         - instance_id:int
#     """

#     try:
#         # getting the transaction instance
#         instance = Transaction.objects.get(pk = instance_id)

#         # getting transaction track ... 
#         trans_track = TransactionTrack.objects.get(user = instance.user)

#         # destructuring transaction track ... 
#         previous_transaction_track = trans_track.previous_transaction_count
#         current_transaction_track = trans_track.current_transaction_count

#         # retrain the model if the current_transaction_track >= previous_transaction_track * 2 
#         # retrain = True if current_transaction_track >= previous_transaction_track * 2 else False

#         # I am retraining everytime so that the model can be more accurate
#         retrain = True

#         # flagging ...
#         transaction_flagging_ml_process(instance_id, retrain)

#         # logging ...
#         logger.info(f"Transaction with the id {instance_id} has been flagged successfully")

#     except AttributeError as e:
#         if "'NoneType' object has no attribute 'predict'" in str(e):
#             self.retry(exc=e, countdown=5)
#     except Exception as e:
#         logger.error(str(e))
    







# def update_user_ml_model_access(user_ids:list, busy_state:bool ):
#     """
#     This function is responsible for activating or deactivating the user profile 'is_model_busy' field which allows/restrict the ml model to classify transactions.
#     """

#     # wrapping the process in atomic so as to handle unforseen errors without destablizing the database 
#     with transaction.atomic():
#         # looping through the ids
#         for user_id in user_ids:
#             user_profile = Profile.objects.filter(user__id = user_id)
            
#             # if user profile does not exist then I am terminating early
#             # This scenario should never exist as the user id is passed automatically without human involvement when creating or retrieving the joblib files

#             if not user_profile.exists():
#                 return 
            
#             # subsetting the user profile
#             user_profile = user_profile[0]

#              # updating the field
#             user_profile.is_ml_model_busy = busy_state

#             # saving the update
#             user_profile.save()

#     logger.info("Profile update ...")

# def create_new_user_ml_model(user_ids:list):
#     """
#     This method is responsible for creating new models for users
#     """
    
#     # Wrapping the ops in an atomic block to enable easy rollback
#     with transaction.atomic():

#         for user_id in user_ids:
#             user_transactions = Transaction.objects.filter(user__id = user_id)

#             # initializing the serializer
#             serializer = ShallowTransactionReadSerializer(instance = user_transactions, many=True)

#             # initializing the transformer to transform the serialized data into a form acceptable by the ml model
#             transformer = DataTransformationEngine(serializer.data)

#             # initializing the ml model
#             ml_model = AnomalyDetectionEngine(transformer.get_df_copy_to_list(["flagged"]), user_id, retrain=True)

#             ml_model.train_model()

#             predictions = ml_model.predict()

#             # looping through the predictions
#             for pred in predictions:

#                 # destructuring each prediction
#                 flagged = pred.get("flagged")
#                 id_ = pred.get("id")

#                 # fetching the matching transactionnn
#                 single_transaction = Transaction.objects.get(pk = id_)

#                 # updating flagged
#                 single_transaction.flagged = flagged

#                 # saving the updated transaction
#                 single_transaction.save()
#     logger.info("Model recreated")




# # this is the main operation
# @shared_task
# def retrain_available_models():
#     """
#     This function is responsible for retraining the models that already exists for eligible user (user with >= 5 transactions)
#     """
#     # ensuring stable db connection
#     close_old_connections()

#     # initializing the model storage processor
#     storage_engine = ModelStorageEngine()

#     # list of the id of eligible user
#     eligible_user_ids = storage_engine.get_all_user_id_from_path()

#     # restricting user access to the ml model
#     update_user_ml_model_access(eligible_user_ids, busy_state=True)

#     # deleting previous ml model
#     storage_engine.clean_up()

#     # creating new ml model for each user
#     create_new_user_ml_model(eligible_user_ids)

#     # allowing user access to the ml model
#     update_user_ml_model_access(eligible_user_ids, busy_state=False)

#     # ensuring stable db connection
#     close_old_connections()
