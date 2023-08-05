import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
# Create your views here.

@api_view(['POST'])
def signup(request):
    data = json.loads(request.body)
    print(data, 'DATA.....')
    try:
        # first_name = data.get("first_name")
        # last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print(user, 'UserDAta ')
        # serialised_profile = UsersSerializer(user, many=False)
        return Response('successful', status=status.HTTP_201_CREATED)
        # return Response("Missing cognito sub attribute", status=status.HTTP_400_BAD_REQUEST)
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        # print(traceback.format_exc())           
        # print("**********************************************************")     
        return Response("Error while fetching or posting user data", status=status.HTTP_400_BAD_REQUEST)