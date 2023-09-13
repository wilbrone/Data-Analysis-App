from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    # path('send_question', send_question, name='send_question'),
    path('send_question', send_question, name='send_question'),
    path('get_user_files', get_user_files, name='get_user_files'),
]