import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate
# Create your views here.

@api_view(['POST'])
def signup(request):
    data = json.loads(request.body)
    try:
        pass
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        # print(traceback.format_exc())           
        # print("**********************************************************")     
        return Response("Error while fetching or posting user data", status=status.HTTP_400_BAD_REQUEST)