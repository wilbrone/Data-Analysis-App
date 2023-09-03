from django.urls import include, path
from .views import *

urlpatterns = [
    path('signup', signup, name='signup'),
    path('send_question', send_question, name='send_question'),
]