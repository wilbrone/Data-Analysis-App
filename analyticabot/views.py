import json
import traceback
import uuid
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from analyticabot.modules.chat_bot import process_question
from analyticabot.modules.messages import save_chat_history

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

global count 
count = 0
data = []

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
def send_question_II(request):
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
        results = process_question(question)

        print('results', results.get('response'))

        response={                            
            "_id": uuid.uuid4(),
            "text": results.get('response'),
            "file": results.get('file'),
            "sessionId": session_id,
        }

        save_chat_history(question, results)
        
        return Response(response, status=status.HTTP_200_OK)
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        print(traceback.format_exc())        
        # print("**********************************************************")    
        return Response("An error occured while sending your question", status=status.HTTP_400_BAD_REQUEST)


def index(request):
    data = "Data was found here"
    return render(request, 'pages/index.html')


def send_question(request):
    global count 
    count += 1

    if request.method == 'POST':
        prompt = request.POST.get('prompt')  # Get the data from the textarea input
        print(prompt, '--------------------#################')
        # Process the prompt data here, e.g., save it to a database, perform some actions, etc.
        # Redirect to a success page or perform any necessary response action
        # return HttpResponseRedirect('/success/')  # Replace '/success/' with your desired success URL

        data = "Try again"

        print(data, '#################')
        # Prepare the data you want to return as JSON
        response_data = {'result': 'Your data processed successfully.', 'data':data}
        
        # return HttpResponse(json.dumps(response_data), content_type="application/json")  # Return JSON responseresponse_data)  # Return JSON response
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    return render(request, 'pages/index.html')  # Replace 'your_template.html' with the actual template name
