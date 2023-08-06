from django.urls import include, path
from .views import get_predicted_questions, signup, send_question

urlpatterns = [
    path('signup', signup, name='signup'),
    path('send_question', send_question, name='send_question'),
    path('get_predictions', get_predicted_questions, name='get_predicted_questions'),
]
