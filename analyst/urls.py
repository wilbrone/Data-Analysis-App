from django.urls import include, path
from .views import signup, send_question

urlpatterns = [
    path('signup', signup, name='signup'),
    path('send_question', send_question, name='send_question'),
]
