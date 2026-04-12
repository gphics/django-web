import boto3
from django.conf import settings
from django.utils import timezone

def get_s3_client() :
    """
    This function configures and generate the s3 client.

    Return:
        boto3.client
    """
    s3_client = boto3.client(
    "s3",
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
    region_name = settings.AWS_S3_REGION_NAME
    )


    return s3_client

def construct_media_url(file_name:str):
    """
    This function constructs the media url

    Param:
        file_name:str

    Return:
        List[public_url, media_key]

    Sample url: https://<bucket-name>.s3.<region>.amazonaws.com/<key>
    """
    time = timezone.now()
    microsecond = time.microsecond
    second = time.second

    # generating media key
    media_key = f"{file_name}_{second}_{microsecond}"

    public_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{media_key}"

    return [public_url, media_key]
