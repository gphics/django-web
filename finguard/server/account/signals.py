from transaction.models import Transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .tasks import update_profile_task

@receiver(sender=Transaction, signal=post_save)
def update_profile_after_save(sender, instance, created, **kwargs):
    """
    This signal fires when a transaction is created
    """
    if created:
        update_profile_task.delay_on_commit(instance.user.pk)

@receiver(sender=Transaction, signal=post_delete)
def update_profile_after_delete(sender, instance,  **kwargs):
        """
        This signal fires when a transaction is deleted
        """
  
        update_profile_task.delay_on_commit(instance.user.pk)
