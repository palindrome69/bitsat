from django.urls import path
from django.conf.urls import url
from main_app.views import *
from django.contrib.auth.decorators import login_required

'''URL configurations for this app

   For more information see:
   https://docs.djangoproject.com/en/2.1/topics/http/urls/

'''
# name used in reverse lookups
app_name = 'main_app'

urlpatterns = [

    path('home/', home, name = 'main_app_home'),
    path('question/<int:pk>/', login_required(QuestionDetailView.as_view()), name = 'question_detail'),
    path('answer/<int:pk>/', answer),
    path('question/delete/<int:pk>/', login_required(DeleteQuestion.as_view()),),
    path('question/<type>/<int:pk>/', vote_question),
    path('answer/<type>/<int:pk>/', vote_answer),
    path('follow/<int:id>/', follow),
    path('unfollow/<int:id>/', unfollow),
    path('user/<int:pk>/', login_required(ProfileView.as_view())),
    path('user/edit/<int:pk>/', ProfileEdit.as_view()),
    path('delete/answer/<int:pk>/', delete_answer),
    path('password/',change_password),
    path('search/',search),
    
]
