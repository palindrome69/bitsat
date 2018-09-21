from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from main_app.forms import *
from main_app.models import *
from django import forms

'''ALL VIEWS TO THIS APP ARE DEFINED HERE.

   For more information to Class Based Views see:
   https://docs.djangoproject.com/en/2.1/topics/class-based-views/

'''

#----------VIEWS RELATED TO USER / Profile---------#

class UserLogin(LoginView):
    '''This is the login page which is the home page as well
    
    '''
    template_name = 'boot.html' # HTML used for this page

class ProfileView(DetailView):
    '''Shows the profile of a user in a web page.
       Shows questions aksed by the user, username and bio.

    '''
    model = Profile

    # Template used to display profile
    template_name = 'main_app/user_detail.html'

class UserCreate(CreateView):
    '''Creates a new User object and its Profile object.

       A view that displays a form for creating an object,
       redisplaying the form with validation errors (if there are any)
       and saving the object.

       If a new User is created successfully, it's Profile
       is also created when get_success_url method is called.

    '''
    form_class = UserForm
    template_name = 'main_app/user_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        '''Adds more data to the context dictionary and
           returns the context dictionary.

        '''
        context = super().get_context_data(*args,**kwargs)
        # Adding user_type and bio fields to the registration page
        context['profile_form'] = ProfileForm()
        return context

    def get_success_url(self):
        '''Creates profile object of the user created then returns
           the success_url.

        '''
        user_type = self.request.POST.get('user_type')
        bio = self.request.POST.get('bio')
        new_Profile = Profile(user = self.object, bio = bio, user_type = user_type)
        new_Profile.save()
        return self.success_url

class ProfileEdit(UpdateView):
    '''A view that displays a form for editing an existing User object,
       redisplaying the form with validation errors (if there are any) and
       saving changes to the object.

       The Profile components (bio) will be updated in the get_success_url method

     '''
    model = User

    # Fields of 'User' model which may be edited
    fields = ['username', 'email',]

    success_url = reverse_lazy('main_app:main_app_home')
    template_name = 'main_app/user_update.html'

    def get(self, request, *args, **kwargs):
        '''Handles a GET request

           Also makes sure that a user cannot access some other user's
           editing page.
           
        '''
        if request.user != User.objects.filter(id = kwargs['pk'])[0]:
            return redirect('/main_app/home')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        '''Updates the bio of the user and returns the success_url.

        '''
        # Profile of the user which is being edited
        profile = self.request.user.profile

        profile.bio = self.request.POST.get('bio')
        profile.save()
        return self.success_url


def change_password(request):
    '''Changes password of the logged in user.

       Displays the form on a 'GET' request and changes the password on a POST request.
       Redirects to the 'main_app/home' if successfully changed else
       back to the password change page.
       Also logs out of all sessions other than current session.

    '''
    form = PasswordChangeForm()

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)

        if form.is_valid():
            # data from the form
            data = form.cleaned_data
            user = authenticate(username = request.user.username,
                                password = data['current_password'] )

            if user:
                # changes password if authenticated 
                user.set_password(data['password1'])
                user.save()
                # logs in again because password was changed
                login(request, user)
                return redirect('main_app:main_app_home')

            else:
                # adds a form error
                form.add_error('current_password', forms.ValidationError('Enter Correct Password'))   

    return render(request, 'main_app/password_change.html',
                 context = {'form':form})        
          
class Logout(LogoutView):
    # Redirects to this url after successfully logged out
    # does a reverse lookup for this string
    next_page = 'home'

#------VIEWS RELATED TO QUESTION-------#

class DeleteQuestion(DeleteView):
    '''A view that displays a confirmation page and deletes an existing object.\

       The given object will only be deleted if the request method is POST.
       If this view is fetched via GET, it will display a confirmation page
       that should contain a form that POSTs to the same URL.

    '''
    model = Question
    template_name = 'main_app/question_confirm_delete.html'
    success_url = reverse_lazy('main_app:main_app_home')
    # TODO -
    #    Remove the confirmation page instead add a popup to confirm

class DeleteAnswer(DeleteView):
    '''A view that displays a confirmation page and deletes an existing object.
    
       The given object will only be deleted if the request method is POST.
       If this view is fetched via GET, it will display a POPUP to confirm
       deletion.
    '''
    model = Answer
    def get_success_url(self):
        
        # ID of the question whose answer is deleted
        question_id = self.object.question.id

        return reverse_lazy('main_app:question_detail',
                            kwargs = {'pk':question_id})

class QuestionDetailView(DetailView):
    '''Inherits from DetailView class.

       This View shows all answers to a given question
       and let's add own answers.
    '''

    model = Question
    template_name = 'main_app/question_detail.html'

    def get(self, request, *args, **kwargs):
        '''Handles GET request.

        '''
        question_id = kwargs['pk']
        question = get_object_or_404(Question, id = question_id)
        profile = request.user.profile

        # makes 'viewed' attribute of all the notifications of this
        # question ONLY for the logged in user equal to True
        for notif in profile.notifications.all():
            if notif.answer in question.answers.all():
                notif.viewed = True
                notif.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''returns context data to be used in template
        
        '''
        context = super().get_context_data(**kwargs)
        # All answers to the question
        context['answerlist'] = self.object.answers.all()
        return context

#----HOME PAGE AND SEARCH--------#

@login_required     #decorator
def home(request):

    '''Home Page of the website when logged in.

       Displays these blocks of questions:
    'Popular'  'questions'  'My Questions'  'New Questions'  'Up Voted'  'Following'
    
    '''
    question_list = Question.objects.order_by('-pub_date')
    questions_by_votes = question_list.order_by('-validity')

    # profile of logged in user
    profile = request.user.profile
    # questions asked by logged in user
    userquestions = profile.questions.all()

    if request.method == 'GET':
            return render(request, 'main_app/question_list.html',
                context = {'question_list':question_list,
                           'question_form':QuestionForm(),
                            'userquestions':userquestions,
                            'questions_by_votes':questions_by_votes})

    # When a question form is submitted (POST request)
    else:
        new_question = request.POST.get('question')
        new_question.strip()
        new_question.capitalize()
        question = Question(question = new_question, author = profile,
                                    pub_date = timezone.now())
        question.save()
        return redirect('/main_app/home')

def search(request):
    '''Searches for a question and returns a new page with results.

       How does it search?

       Takes one word at a time from the search query and
       if the word is not in the COMMON_WORDS list
       and it is not a single letter, it is searched
       in all questions in the database.
       Questions containing this word are returned.
       It continues until all words are searched.
      
    '''
    # List of commonly used words  
    COMMON_WORDS = ['why', 'how', 'what', 'is', 'are',
                   'or', 'when', 'whom', 'where', 'that',
                   'to', 'i', 'am', 'up', 'an' ]

    # Gets query, this is what the user searched.
    query = request.GET.get('query')
    query.strip()

    # if search query is blank
    if len(query) == 0:
        # previous page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        pass    
    
    # removes question mark
    if query[-1] == '?': query = query[:-1]
    else: pass    

    # list of all words in query   
    query_words = query.split(" ")
    query_words = [word.lower() for word in query_words]

    results = []

    # Finds results
    for word in query_words:
        if word not in COMMON_WORDS and len(word) > 1:
            matches = Question.objects.filter(question__contains = word)
            for match in matches:
                if match not in results:
                    results.append(match)
                else:
                    pass    
        else:
            pass
    return render(request, 'main_app/search_result.html',
                 context = {'results' : results})

#------VIEWS RELATED TO ANSWER---------#

@login_required     #decorator.
def answer(request, **kwargs):
    '''handler when a user answers a question
    
       Creates Notification for the users following
       the question and the user who posted the question.
       Notification will not be created for the author if
       the author of the question answers his own question.
    
    '''
    question_id = kwargs['pk']
    question = get_object_or_404(Question, id = question_id)
    profile = request.user.profile

    # if answer area is not left blank
    if request.POST.get('answer'):
        ans = request.POST.get('answer')
        ans.strip()
        answer = Answer(answer = ans, pub_date = timezone.now(),
                        author = profile, question = question)
        answer.save()
        Notification.create_notif(question, answer, profile)

    else:
        pass

    last_page = request.META.get("HTTP_REFERER")
    return redirect(last_page)

#------FOLLOWING AND UNFOLLOWING-----#

@login_required    #decorator
def follow(request, **kwargs):
    '''Handles following of a question.
       Returns to the previous page if successfully followed.

    '''
    question_id = kwargs['id']
    question = get_object_or_404(Question, id = question_id)
    profile = request.user.profile

    # Adds the user to the following list
    question.following.add(profile)
    question.save()

    last_page = request.META.get('HTTP_REFERER')
    return redirect(last_page)

def unfollow(request, **kwargs):
    '''Handles unfollowing of a question.

    '''
    question_id = kwargs['id']
    question = get_object_or_404(Question, id = question_id)
    profile = request.user.profile

    # removes the profile(user) from the following list
    question.following.remove(profile)
    question.save()

    last_page = request.META.get('HTTP_REFERER')
    return redirect(last_page)

#------VOTE------#

@login_required     # decorator
def vote(request, **kwargs):
    '''handler when a user votes on a question'''

    question_id = kwargs['pk']
    vote_type = kwargs['type']
    question = get_object_or_404(Question, id = question_id)
    profile = request.user.profile

    # will be an empty queryset if not voted before else will have just one object
    previously_voted = Vote.objects.filter(question = question, user = profile)

    if not previously_voted:
        # if no previous vote, a new vote object will be created
        new_vote = Vote(question = question, user = profile, type = vote_type)
        new_vote.save()
    else:
        previous_vote = previously_voted[0]
        # previous vote object is updated
        previous_vote.type = vote_type
        previous_vote.save()

    # updates the difference between upvotes and downvotes
    question.validity = (len(question.votes.filter(type = 'Upvote')) -
                         len(question.votes.filter(type = 'Downvote')))
    question.save()

    last_page = request.META.get('HTTP_REFERER')
    return redirect(last_page)
