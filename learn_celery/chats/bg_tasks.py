from celery import shared_task
from .models import Comment, Post,Like
from celery.utils.log import get_task_logger
from pathlib import Path
from django.utils import timezone
import shutil

base_dir = Path(__file__).resolve().parent
logger = get_task_logger(__name__)

@shared_task
def add_comment(messages:list, post_id:int):

    Comment.objects.create(messages=messages, post=Post.objects.get(pk=post_id))

    logger.info("Comment created ...")

# @shared_task
# def initiate_dir():
#     Path.mkdir(f"{base_dir}/location_store")
#     logger.info("DIRECTORY CREATED")

@shared_task
def create_log_file():
    time = timezone.now()
    minute = time.minute
    second = time.second
    file_path = Path(f"{base_dir}/location_store/log_{minute}_{second}.txt")

    file_path.write_text(f"The time is {time.isoformat()}")

    logger.info("LOG FILE CREATED")

@shared_task
def clean_up():

    dir_path = Path(f"{base_dir}/location_store")

    if dir_path.exists():
        shutil.rmtree(dir_path)

    dir_path.mkdir()


    logger.info("CLEANING UP ...")