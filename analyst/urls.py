from django.urls import include, path
from .views import get_predicted_questions, send_general_question, signup, send_question

urlpatterns = [
    path('signup', signup, name='signup'),
    path('send_question', send_question, name='send_question'),
    path('get_predictions', get_predicted_questions, name='get_predicted_questions'),
    path('send_general_question', send_general_question, name='send_general_question'),
]
