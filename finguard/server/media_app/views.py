from rest_framework.response import Response
from rest_framework.request import Request
from utils import get_s3_client, construct_media_url
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.conf import settings
from utils.res import generate_res
from .models import Media
from transaction.models import Circle
from rest_framework import status
from .serializers import MediaSerializer
bucket_name = settings.AWS_STORAGE_BUCKET_NAME


class MediaUploadView(APIView):
    
    acceptable_mimetypes = [
    "image/png",     
    "image/jpg",     
    "image/jpeg",     
    "image/gif",   
    "image/webp",   
    "image/svg+xml",
    "image/svg", 
    ]

    def get(self, request:Request):
        """
        # This is just for testing purpose
        """

        media = Media.objects.all()

        serializer = MediaSerializer(instance = media, many=True)

        return Response(serializer.data)

    def post(self, request:Request):
        """
        # This route is for uploading file(images)

        ## Request params:
            - media -> file

        ## Request query:
            id?:int --> circle id. All circle members can update circle profile
      
        ### s3_client.upload_fileobj
            - fileobj
            - bucket name
            - key (personally constructed)
            - {ContentType}

        ## Return : success message if no error
        """
        try:
            # getting circle id if it exist
            circle_id = request.query_params.get("id", None)

            # getting the uploaded file(image)
            media = request.data.get("media", None)

            # validating media
            if not media:
                return Response(generate_res(err={"msg":"image file must be uploaded"}), status=status.HTTP_400_BAD_REQUEST)
            
            mimetype = media.content_type
            media_name = media.name
            
            # validating mimetype
            if mimetype not in self.acceptable_mimetypes:
                return Response(generate_res(err={"msg":f"{mimetype} format not acceptable"}), status=status.HTTP_400_BAD_REQUEST)
            
            # validating circle id
            circle = None
            if circle_id:
                circle = Circle.objects.filter(pk = circle_id)
                if not circle.exists():
                    return Response(generate_res(err={"msg":f"Circle does not exist"}), status=status.HTTP_400_BAD_REQUEST)
                
                # subsetting circle
                circle = circle[0]

                # validating auth user permission
                is_member = circle.is_member(user = request.user)
                if not is_member:
                    return Response(generate_res(err={"msg":"Unauthorized action"}), status=status.HTTP_401_UNAUTHORIZED)

            # getting the configured s3 client
            media_client= get_s3_client()
            public_url, media_key = construct_media_url(media_name)
            
            # uploading file to s3
            media_client.upload_fileobj(
                media,
                bucket_name,
                media_key,
                {"ContentType":mimetype}
            )

            # FINAL OPs
            if circle_id:
                # saving the file details
                Media.objects.create(media_key = media_key, public_url=public_url, circle=circle)
            else:
                # saving the file details
                Media.objects.create(media_key = media_key, public_url=public_url, user_profile=request.user.profile)

            return Response({"msg":"image uploaded successfully"})
        
        except Exception as e:
            return Response(generate_res(err={"msg":str(e)}))
    

    def put(self, request:Request):
        """
        # This method is for updating (delete and upload) an existing media

        ## Request param:
            - media: file
        
        ## Request query:
            - id:int -> media id

        ## Return:
            - a success message if no error
        """
        try:
            media_id = request.query_params.get("id", None)

            # validating media id
            if not media_id:
                return Response(generate_res(err={"msg":"media id must be provided"}), status=status.HTTP_400_BAD_REQUEST)
            
            media = request.data.get("media", None)

            # validating media
            if not media:
                return Response(generate_res(err={"msg":"image file must be uploaded"}), status=status.HTTP_400_BAD_REQUEST)
            

            media_name = media.name
            mimetype =media.content_type

            # validating mimetype
            if mimetype not in self.acceptable_mimetypes:
                return Response(generate_res(err={"msg":f"{mimetype} format not acceptable"}), status=status.HTTP_400_BAD_REQUEST)
            
            # getting media instance
            media_instance = Media.objects.filter(pk = media_id)
            
            if not media_instance.exists():
                return Response(generate_res(err={"msg":"media does not exist"}), status=status.HTTP_404_NOT_FOUND)
            
            media_instance = media_instance[0]

            # creating new url and key
            public_url, media_key = construct_media_url(media_name)

            media_client = get_s3_client()

            # uploading new obj
            media_client.upload_fileobj(
                media,
                bucket_name,
                media_key,
                {"ContentType":mimetype}
            )

            # deleting previous obj
            media_client.delete_object(
                Bucket = bucket_name,
                Key = media_instance.media_key
            )

            # saving new data
            media_instance.media_key = media_key
            media_instance.public_url = public_url

            # saving ...
            media_instance.save()

            return Response(generate_res({"msg":"media updated successfully"}))
        except Exception as e:
            return Response(generate_res({"msg":str(e)}))
       