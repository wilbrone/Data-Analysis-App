import json
import traceback
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from analyst.modules.chat_bot import chat_bot_qeustion_predictions, process_user_query, send_to_format_response, send_to_general

# Create your views here.
results = None
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
        user = authenticate(username=username, password=password)
        login(request, user)
        print(user, '########################', login(request, user))
        # serialised_profile = UsersSerializer(user, many=False)
        return Response(f'{user} successfully saved', status=status.HTTP_201_CREATED)
        # return Response("Missing cognito sub attribute", status=status.HTTP_400_BAD_REQUEST)
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        print(traceback.format_exc())           
        # print("**********************************************************")     
        return Response("Error while fetching or posting user data", status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def send_question(request):
    results = None
    try:
        question_type = request.data.get("questionType")
        user_id = request.data.get("userId")        
        session_id = request.data.get("sessionId")
        question = request.data.get("question")

        if user_id is None or user_id < 0:
            return Response("Missing User ID", status=status.HTTP_400_BAD_REQUEST)
        if question_type=="text":
            question = request.data.get("question")                                                
            if isinstance(question, str)==False or len(question) == 0:
                return Response("Seems like you sent an empty message :(", status=status.HTTP_200_OK)
        elif question_type=="audio": 
            return Response("Mmmmmh, Thank you for trying our audio message feature, unfornately we are still perfcting it...", status=status.HTTP_200_OK)                                                  

        # We will be getting or creating the chat history
        # call a function from the message modules folder
        results = process_user_query(question)
        

        print(results, 'results')
                                                        
        response={                            
            "_id": uuid.uuid4(),
            "text": results.response,
            "sessionId": session_id,
        } 
        return Response(response, status=status.HTTP_200_OK)
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        print(traceback.format_exc())        
        # print("**********************************************************")    
        return Response("An error occured while sending your question", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_predicted_questions(request):
    session_id = request.data.get("sessionId")
    print(session_id, 'session_id')
    
    try:
        
        results = chat_bot_qeustion_predictions()
        print(results, 'results**********')
                                                 
        response={                            
            "text": results.response,
            "sessionId": session_id,
        } 
        print(response, '-------________--------**______**response')
        return Response(response, status=status.HTTP_200_OK)
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        print(traceback.format_exc())        
        # print("**********************************************************")    
        return Response("An error occured while getting predictions", status=status.HTTP_400_BAD_REQUEST)
