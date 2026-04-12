# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import Comment
# from .bg_tasks import create_likes


# def main_ops(comment):
#     # create_likes(comment)
#     pass

# @receiver(signal=[post_save], sender=Comment)
# def create_likes_in_bg(sender, created, instance, **kwargs):
#     if created:
#         main_ops(instance)
