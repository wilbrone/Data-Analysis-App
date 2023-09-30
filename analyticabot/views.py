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

from analyticabot.modules.utils import delete_media_file, list_media_files
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.conf import settings

from .form import FileUploadForm

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

            save_chat_history(question, results.get('response'))
            
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
    # if request.method == 'POST':
    #     print('request.POST', request.POST)
    #     form = FileUploadForm(request.POST, request.FILES)
    #     print('form', form, form.is_valid())
    #     if form.is_valid():
    #         print('form.is_valid')
    #         # 
    #         handle_uploaded_file(request.FILES['file'])
    #         return render(request, 'file_uploaded.html')
    #     else:
    #         print('else---------')
    #         # 
    #         form = FileUploadForm()
    # else:
    #     print('else')
    #     # 
    form = FileUploadForm()
    # return render(request, 'pages/index.html', {'form': form})
    return render(request, 'pages/index.html', {'mode': mode, 'form': form})


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
    print('ÄÄÄÄÄÄÄÄÄÄÄÄ', request.FILES)

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
        

        # question = "You are an AI assistant in the field of data science. Learn everything you need to know and all the techniques of cleaning a dataset. Use this knowledge and everything in your capacity to clean the dataset, print out the updated data in a file and save locally in the media folder (settings.MEDIA_ROOT) use PIL. Handle missing values by removing the rows with missing values. Do not exclude or interfere with the columns with date and time in your execution"
        # results = process_question(question, uploaded_file.name)

        # print(file_path, '###########################', results.get('response'))

        codebox_folder = os.path.join(settings.BASE_DIR, '.codebox')

        for filename in os.listdir(codebox_folder):
            print(filename, 'eeeerererererrhëëëëëë')

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
    

# @api_view(['POST'])
def upload_file(request):
    mode = settings.MODE
    file_name = ''
    print('ÄÄÄÄÄÄÄÄÄÄÄÄ---Checking for file in request.FILES = ', 'file' in request.FILES, 'request.POST----->', request.POST, 'request.FILES', request.FILES, request.FILES['file'])

    # print('ÄÄÄÄÄÄÄÄÄÄÄ---Getting uploaded file', request.FILES['file'])
    try:
        if request.method == 'POST':
            file = request.FILES['file']
            print('ÄÄÄÄÄÄÄÄÄÄÄ---Checking the file', file)
            if file:
                file_name = file.name
                
                # process the file
                delete_media_file()

                print("process the file")
                file_format = get_file_format(file_name)
                if file_format == '.csv' or file_format in ('.xls', '.xlsx', '.xlsb', '.xlsm'):
                    handle_uploaded_file(request.FILES['file'])
                else:
                    print('#######---- The file is in Excel format.')
                    form = FileUploadForm()
                    return render(request, 'pages/index.html', {'message':'please attach a file', 'form':form})
                form = FileUploadForm()
                return render(request, 'pages/index.html', {'mode':mode, 'file':file_name, 'form':form})
                ...
            else:
                # handle the case where no file was provided
                form = FileUploadForm()
                print("handle the case where no file was provided")
                ...

            # form = FileUploadForm(request.POST, request.FILES)
            # print('ÄÄÄÄÄÄÄÄÄÄÄ---Checking the form ', form)
            # if form.is_valid():

            #     handle_uploaded_file(request.FILES['file'])
            #     return render(request, 'pages/index.html', {'mode':mode, 'file':file_name})
            
        else:
            form = FileUploadForm()

        return render(request, 'pages/index.html', {'form': form, 'mode':mode, 'file':file_name})
    except:
        form = FileUploadForm()
        return render(request, 'pages/index.html', {'form': form, 'mode':mode, 'file':file_name})
    
def handle_uploaded_file(f):
    # with open(os.path.join('media', f.name), 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
    print('ÄÄÄÄÄÄÄÄÄÄÄÄ', f.name)
    media_root = settings.MEDIA_ROOT
    
    # Create a directory based on the user ID if it doesn't exist
    user_folder_path = os.path.join(media_root, 'user_id')
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
    
    # Save the uploaded file to the user's folder
    file_path = os.path.join(user_folder_path, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def get_file_format(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower()