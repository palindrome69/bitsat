from django.urls import path
from django.conf.urls import url
from main_app.views import *
from django.contrib.auth.decorators import login_required

'''main_app url configuration
all url patterns for the site particularly for this app
url follows as example -->"https://domain.com/main_app/home"  for the name main_app_home
----------------------------------------------------------------------------------------
@variables
urlpatterns --> List of all urls.
app_name --> This is the name by which the urls of THIS app can
             be referred in the 'reverse' method.
             'reverse(app_name:url_name)'.
             *works for reverse_lazy as well.

'''

app_name = 'main_app'
urlpatterns = [

    path('home/', main_app_view, name = 'main_app_home'),
    path('question/<int:pk>/', login_required(QuestionDetailView.as_view()), name = 'question_detail'),
    path('answer/<int:pk>/', answer),
    path('question/delete/<int:pk>/', login_required(DeleteQuestion.as_view()),),
    path('question/<type>/<int:pk>/', vote),
    path('follow/<int:id>/', follow),
    path('unfollow/<int:id>/', unfollow),
    path('user/<int:pk>/', login_required(ProfileView.as_view())),
    path('user/edit/<int:pk>/', ProfileEdit.as_view()),
    path('answer/delete/<int:pk>/', DeleteAnswer.as_view()),
    path('password/',change_password),
    path('search/',search),



]
