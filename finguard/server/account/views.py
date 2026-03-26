from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import (UserSerializer, ProfileSerializer)
from utils.res import generate_res
from django.db import transaction
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from babel.core import get_global


#  USER (AUTH) ...

@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    """
    This is the user and default profile creation view. It 

    Request Data:
        username
        password
    Return:
        It return the user auth token
    """

    # verifying if auth user already exists
    if request.user.is_authenticated:
        return Response(generate_res(err={"msg":"You are already authenticated"}))
    
    # creating serializer
    serializer = UserSerializer(data = request.data)

    if serializer.is_valid():
        # creating atomic transaction to make sure the two process was successful
        with transaction.atomic():
            user = serializer.save()
            Profile.objects.create(user = user)

            token = Token.objects.get_or_create(user = user)
            
           
        return Response(generate_res({"msg":{
            "token":str(token[0])
        }}))
    # print(serializer.errors)
    return Response(generate_res(err={"msg" : serializer.errors}), status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def auth_user(request):
    """
    The login view

    Request Data:
        username
        password

    Return:
        auth token
    """
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if not username or not password:
        return Response(generate_res(err={"msg":"password and username must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password = password)
    if user:
        token = str(Token.objects.get_or_create(user = user)[0])

        return Response(generate_res({"token":token}))
    return Response(generate_res(err={"msg":"invalid credentials"}), status=status.HTTP_400_BAD_REQUEST)


#
#
# PROFILE ...

class ProvileView(APIView):
    """
    This class view handles all CRUD ops for both profile and user model
    """
    def get(self, request):
        """
        This is the read view. It get the profile data of the logged in user

        Request param:
            search (optional): user id (int) | all (to get all users)

        Return:
            user(s) profile
        """
        search = request.query_params.get("search", None)
        if not search:
            user = request.user
            serializer = ProfileSerializer(instance = Profile.objects.get(user = user))
            
        elif search == "all":
            serializer = ProfileSerializer(instance = Profile.objects.all(), many = True)
        else:
            try:
                user = User.objects.get(pk = int(search))
            except Exception as e:
                return Response(generate_res(err={"msg": str(e)}), status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(instance = Profile.objects.get(user = user))
        return Response(generate_res({"msg":serializer.data}))

    def put(self, request):
        """
        This is update route for basic information update for profile and user. email, username and password cannot be changed here.
        """

        # previous user info
        req_user = request.user
        req_profile = Profile.objects.get(user = req_user)

        # selecting the data from the request object
        user = request.data.get("user", {})
        profile = request.data.get("profile", {})

        # filtering out email and username
        if user.get("username") or user.get("email"):
            return Response(generate_res(err={"msg":"action not allowed"}), status=status.HTTP_400_BAD_REQUEST)

        # serializers
        user_ser = UserSerializer(instance = req_user, data = user, partial = True)
        profile_ser = ProfileSerializer(instance = req_profile, data = profile, partial = True)
        
        # validating and saving
        if user_ser.is_valid() and profile_ser.is_valid():
            with transaction.atomic():
                user_ser.save()
                profile_ser.save()
            return Response(generate_res(data={"msg": "user profile updated successfully"}))
        else:
            return Response(generate_res(err={user_ser.errors or None, profile_ser.errors or None}), status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_all_currencies(request):
    """
    ShallowThis view returns all currencies codes and symbols

    """

    all_currencies = get_global("all_currencies")

    return Response(generate_res({"msg": all_currencies}))
    
@api_view(["PUT"])
def update_password(request):
    """
    This view is for updating the password

    Request data:
        old_password
        new_password

    Return:
        auth token
    """
    user = request.user
    old_password  =  request.data.get("old_password", None)
    new_password  =  request.data.get("new_password", None)

    # validations
    if not old_password or not new_password:
        return Response(generate_res(err={"msg":"Both old and new password must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    if len(str(new_password)) < 6:
        return Response(generate_res(err={"msg":"New password length must be greater than 5"}), status=status.HTTP_400_BAD_REQUEST)
    
    # making sure the old password provided is the actual previous password
    is_old_password = user.check_password(old_password)

    # making sure the new password is not the same with the old password
    is_password_unavailable = user.check_password(new_password)
    
    if not is_old_password:
        return Response(generate_res(err={"msg":"The old password is not correct"}), status=status.HTTP_400_BAD_REQUEST)
    
    if is_password_unavailable:
        return Response(generate_res(err={"msg":"The old password and new password must be different"}), status=status.HTTP_400_BAD_REQUEST)
    
    # saving the new password
    user.set_password(str(new_password))
    user.save()
    
    return Response(generate_res({"msg":"password updated successfully"}))


@api_view(["PUT"])
def update_username(request):
    """
    This view is for updating the username

    Request data:
        username
    Return:
        auth token
    """
    username = request.data.get("username", None)
    if not username:
        return Response(generate_res(err={"msg":"username must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    
    # checking email availability
    is_unavailable = User.objects.filter(username = username).exists()
    if is_unavailable:
        return Response(generate_res(err={"msg":"user already exist"}), status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    user.username = username
    user.save()

    return Response(generate_res({"msg":"username updated successfully"}))



@api_view(["PUT"])
def update_email(request):
    """
    This view is for updating the user email

    Request data:
        email

    Return:
        auth token
    """
    email = request.data.get("email", None)
    if not email:
        return Response(generate_res(err={"msg":"email must be provided"}), status=status.HTTP_400_BAD_REQUEST)
    
    # checking email availability
    is_unavailable = User.objects.filter(email = email).exists()
    if is_unavailable:
        return Response(generate_res(err={"msg":"user already exist"}), status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    user.email = email
    user.save()

    return Response(generate_res({"msg":"email updated successfully"}))