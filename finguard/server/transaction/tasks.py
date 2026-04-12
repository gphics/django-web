from celery import shared_task
from .models import Transaction
from typing import Callable
@shared_task
def handle_transaction_post_save(func:Callable[[Transaction], None], transaction_instance:Transaction):
    """
    This function handles the post save signal operation for the transaction model in the background so the app can be more faster

    Param:
        func: the main function from the signal
        transaction_instance
    """
    # calling the passsed function
    func(transaction_instance)