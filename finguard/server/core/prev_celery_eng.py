import os
from celery import Celery
from celery.signals import task_postrun
from django.db import connections
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

@task_postrun.connect
def close_db_connections(*args, **kwargs):
    """
    Forces all Django database connections to close 
    immediately after any Celery task finishes executing.
    """
    for conn in connections.all():
        conn.close()

celery_app = Celery("core")

celery_app.config_from_object("django.conf.settings", namespace="CELERY")

celery_app.autodiscover_tasks()