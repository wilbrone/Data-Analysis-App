import json
import os
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

from analyticabot.modules.utils import list_media_files
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.conf import settings

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
def send_question(request):
    results = None
    try:
        if request.method == 'POST':
            user_message = json.loads(request.body.decode('utf-8'))['message']
            question_type = user_message.get("questionType")
            user_id = user_message.get("userId")        
            session_id = user_message.get("sessionId")
            question = user_message.get("question")
            file = user_message.get("file")

            print(question, isinstance(question, str), type(question))

            if user_id is None or user_id < 0:
                return Response("Missing User ID", status=status.HTTP_400_BAD_REQUEST)
            if question_type=="text":
                # question = request.data.get("question")                                                
                if isinstance(question, str)==False or len(question) == 0:
                    return Response("Seems like you sent an empty message :(", status=status.HTTP_200_OK)
            elif question_type=="audio": 
                return Response("Mmmmmh, Thank you for trying our audio message feature, unfornately we are still perfcting it...", status=status.HTTP_200_OK)                                                  

            # We will be getting or creating the chat history
            # call a function from the message modules folder
            results = process_question(question, file)

            print('results', results.get('response'))

            response={                            
                "_id": uuid.uuid4(),
                "text": results.get('response'),
                "file": results.get('file'),
                "sessionId": session_id,
            }

            save_chat_history(question, results)
            
            # return Response(response, status=status.HTTP_200_OK)
            return JsonResponse({'response': response})
    except:
        # Unmuted to see full error !!!!!!!!!
        # print("**********************************************************")
        print(traceback.format_exc())        
        # print("**********************************************************")    
        return Response("An error occured while sending your question", status=status.HTTP_400_BAD_REQUEST)


def index(request):
    data = "Data was found here"
    mode = settings.MODE
    return render(request, 'pages/index.html', {'mode': mode})


def send_question_II(request):
    global count 
    count += 1

    if request.method == 'POST':
        # Process the user's message
        user_message = json.loads(request.body.decode('utf-8'))['message']
        print(user_message, 'ÄÄÄÄÄÄÄÄ')
        # Generate a response
        ai_response = "This is the response from the AI."

        # Return the response as JSON
        return JsonResponse({'response': ai_response})
    

def get_user_files(request):
    if request.method == 'GET':
        # Get the list of file names in the media folder
        media_files = list_media_files()

        # You can now pass this list to your template context
        context = {
            'media_files': media_files,
        }

        return JsonResponse({'response': context})



def upload_view(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        print(uploaded_file, 'ÄÄÄÄÄÄÄÄÄÄÄÄ', uploaded_file.name)

        media_root = settings.MEDIA_ROOT
    
        # Create a directory based on the user ID if it doesn't exist
        user_folder_path = os.path.join(media_root, 'user_id')
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
        
        # Save the uploaded file to the user's folder
        file_path = os.path.join(user_folder_path, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        

        question = ""
        process_question(question, uploaded_file.name)

        print(file_path)
        # If you want to save the file to the database, create a new UploadedFile instance and save it.
        # uploaded_file_instance = UploadedFile(file=uploaded_file)
        # uploaded_file_instance.save()
        
        # You can also save the file to a specific directory.
        # file deepcode ignore PT: <please specify a reason of ignoring this>
        # with open('uploads/' + uploaded_file.name, 'wb+') as destination:
        #     for chunk in uploaded_file.chunks():
        #         destination.write(chunk)
        
        return JsonResponse({'message': 'File uploaded successfully', 'file_name': uploaded_file.name})
    else:
        return JsonResponse({'message': 'No file provided'}, status=400)