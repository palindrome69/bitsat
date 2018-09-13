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
from main_app.forms import QuestionForm, UserForm, ProfileForm,PasswordChangeForm
from main_app.models import Profile, Question, Answer, Vote, Notification
from django import forms

''' ALL VIEWS TO THIS APP ARE DEFINED HERE.

'''
class UserLogin(LoginView):
    '''This is the login page which is the home page as well'''
    template_name = 'boot.html' # HTML used for this page

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
       If this view is fetched via GET, it will display a confirmation page
       that should contain a form that POSTs to the same URL
    '''
    model = Answer
    def get_success_url(self):
        # ID of the question whose answer is deleted
        question_id = self.object.question.id
        # returns to that question's detail view
        return reverse_lazy('main_app:question_detail',
                            kwargs = {'pk':question_id})

@login_required     #decorator
def main_app_view(request):

    '''Home Page of the website when logged in.
    Displays the list of all questions as well as another block with
    the question asked by the user which is logged in.
    ----------------------------------------------------------------
    @VARIABLES
        question_list : list
                        List containing all questions in database.

        user_list     : List
                        List containing all Profiles in database.


        userquestions : list
                        List containing Questions asked by the logged in user.

        Profile       : Profile
                        Profile of the logged in user.

        context       : Dict
                        Dictionary which holds all the context data.

        question      : str
                        String which is the new question asked by the logged in user
                        upon POST request.

        new_question  : Question
                        object of Question class which is the new question asked.
    '''

    question_list = list(Question.objects.all())
    question_list.reverse()
    profile = Profile.objects.filter(user = request.user)[0]
    userquestions = profile.questions.all()

    if request.method == 'GET':
            return render(request, 'main_app/question_list.html',
                context = {'question_list':question_list,
                           'profile':profile,
                           'question_form':QuestionForm(),
                            'userquestions':userquestions})

    # When a question form is submitted (POST request)
    else:
        new_question = request.POST.get('question')
        # makes the first character of question uppercase
        new_question = new_question.capitalize()
        new_question = Question(question = new_question, author = profile,
                                    pub_date = timezone.now())
        # saves new question to database
        new_question.save()
        return redirect('/main_app/home')


class QuestionDetailView(DetailView):

    '''Inherits from DetailView class.
       This View shows all answers to a given question
       and lets add own answers.
       -----------------------------------------------
       @VARIABLES
                model : Question
                    Model class of the object in use
                self.object : Question
                    object in use (a question in this case)
                template_name : str
                        Html used for this page
    '''

    model = Question
    template_name = 'main_app/question_detail.html'

    def get(self, request, *args, **kwargs):
        '''Handles GET request.

        '''

        # id of the question viewing
        question_id = kwargs['pk']

        # question viewing returns a 404 error if not found
        question = get_object_or_404(Question, id = question_id)

        # Profile of the logged in user
        profile = get_object_or_404(Profile, user = request.user)

        # makes 'viewed' attribute of all the notifications of this
        # question for the logged in user equal to 'viewed'
        for notif in profile.notifications.all():
            if notif.answer in question.answers.all():
                notif.viewed = True
                notif.save()

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        '''returns context data to be used in template'''
        # Gets context data which is added by the superclass
        context = super().get_context_data(**kwargs)

        # adds the reference to the profile of logged in user
        context['profile'] = Profile.objects.get(user = self.request.user)

        # adds more data to the context dictionary
        context['answerlist'] = self.object.answers.all()

        return context



# TODO: Change this to Profile View
class UserDetailView(DetailView):
    '''View which shows the profile of a user in a web page.
       Shows questions aksed by the user, username and bio.
    '''
    model = Profile
    # Template used to display profile
    template_name = 'main_app/user_detail.html'


@login_required     #decorator.
def answer(request, **kwargs):
    '''handler when a user answers a question'''

    # ID(PrimaryKey) of the question which is answered
    quetion_id = kwargs['pk']

    # Question to which answer is posted
    ques = Question.objects.filter(id = quetion_id)[0]

    # Current logged in user
    profile = Profile.objects.filter(user = request.user)[0]

    # validates if answer is not blank
    if request.POST.get('answer'):
        ans = request.POST.get('answer')
        answer = Answer(answer = ans, pub_date = timezone.now(),
                        author = profile, question = ques)
        answer.save()
        following_users = ques.following.all()
        author = ques.author

        # create notification to the author of question.
        # creates notif only when someone else answers on your question
        if author != profile:
            author_notif = Notification(to = author, by = profile,
                                        answer = answer, date = timezone.now())
            author_notif.save()

        # Creates notification to users following the question
        for user in following_users:
            # Create notif only when someone other than author of question answers.
            if user != profile and user != author:
                followers_notif = Notification(to = user, by = profile,
                                               answer = answer, date = timezone.now())
                followers_notif.save()
    else:
        pass

    last_page = request.META.get("HTTP_REFERER")
    return redirect(last_page)

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

    # Overrides get_context_data method to add more data to context
    def get_context_data(self, *args, **kwargs):
        '''Adds more data to the context dictionary and
           returns the context dictionary.

        '''
        context = super().get_context_data(*args,**kwargs)
        # Adding user_type and bio fields to the registration page
        context['profile_form'] = ProfileForm()
        return context

    def get_success_url(self):
        '''Creates profile of the new user created then returns
           the success_url.

        '''
        user_type = self.request.POST.get('user_type')
        bio = self.request.POST.get('bio')
        new_Profile = Profile(user = self.object,bio = bio, user_type = user_type)
        new_Profile.save()
        return self.success_url

@login_required    #decorator
def follow(request, **kwargs):
    '''Handles following of a question.
       Returns to the previous URL if successfully followed.

    '''

    # ID of the question followed
    question_id = kwargs['id']

    # Question which is followed
    question = Question.objects.filter(id = question_id)[0]

    # Profile of the user which followed the question (Logged in user)
    profile = Profile.objects.filter(user = request.user)[0]

    # Adds the user to the following
    question.following.add(profile)
    question.save()
    last_page = request.META.get('HTTP_REFERER')

    return redirect(last_page)

def unfollow(request, **kwargs):
    '''Handles unfollowing of a question

    '''
    # ID of the question followed
    question_id = kwargs['id']

    # Question which is followed
    question = Question.objects.filter(id = question_id)[0]

    # Profile of the user which followed the question (Logged in user)
    profile = Profile.objects.filter(user = request.user)[0]

    # removes the profile(user) from the following list
    question.following.remove(profile)
    question.save()

    # page from which question was 'unfollowed'
    last_page = request.META.get('HTTP_REFERER')

    return redirect(last_page)


class ProfileEdit(UpdateView):
    '''A view that displays a form for editing an existing User object,
       redisplaying the form with validation errors (if there are any) and
       saving changes to the object.

       The Profile components (bio) will be updated in the get_success_url method

     '''
    model = User
    # Fields of 'User' model which may be edited
    fields = ['username', 'email',]

    # returns to this url after successfully edited
    success_url = reverse_lazy('main_app:main_app_home')

    # tempate used for editing
    template_name = 'main_app/user_update.html'

    # TODO: implement GET OBJECT OR 404
    def get(self, request, *args, **kwargs):
        '''Handles a GET request

           Also makes sure that a user cannot access some other user's
           editing page.
        '''

        # if logged in user is not same as the user being edited
        if request.user != User.objects.filter(id = kwargs['pk'])[0]:
            return redirect('/main_app/home')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        '''Updates the bio of the user and returns the success_url.
        '''
        # Profile of the user which is being edited
        profile = Profile.objects.filter(user = self.object)[0]

        # Checks if the bio field is left blank
        if not self.request.POST.get('bio'):
            # assigns it to a blank string
            profile.bio = ""
        else:
            # updates bio
            profile.bio = self.request.POST.get('bio')

        profile.save()
        return self.success_url

    def get_context_data(self, *args, **kwargs):
        '''Adds more data to context dictionary and returns it

        '''
        context = super().get_context_data(*args, **kwargs)
        # Adds the profile of the user being edited
        context['profile'] = Profile.objects.filter(user = self.object)[0]
        return context

@login_required     # decorator
def vote(request, **kwargs):
    '''handler when a user votes on a question'''

    question_id = kwargs['pk']
    vote_type = kwargs['type']

    # question object of question which is voted
    question = Question.objects.filter(id = question_id)[0]

    # profile of the user which voted on the question
    profile = Profile.objects.filter(user = request.user)[0]

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


def change_password(request):
    '''Changes password of the logged in user.
       
       Displays the form on a 'GET' request and changes the password on a POST request.
       Redirects to the 'main_app/home' if successfully changed.
       Also logs out of all sessions other than current session.

    '''   
    if request.method == 'GET':
        # Displays the form
        return render(request, 'main_app/password_change.html',
                      context={'form':PasswordChangeForm()})

    else:

        # password 1 and password 2 are fields for new password and its confirmation
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # username of the logged in user
        username = request.user.username

        # current password for the user
        current_password = request.POST.get('current_password')

        # Checks the equality of the new password in both password fields
        if password1 != password2:
            print("passwords don't match")
            return redirect('/main_app/password')
        else:
            pass    

        # checks if the current password entered is correct.
        # Returns a user object if correct else None
        user = authenticate(request, username = username, password = current_password)

        if not user:
            print('Incorrect Password')
            return redirect('/main_app/password')
        else:
            pass    

        # Sets new password for the logged in users
        user = request.user    
        user.set_password(password1)
        user.save()

        # logs in for current session as password is changed
        login(request, user)

        return redirect('/main_app/home')

class Logout(LogoutView):
    # Redirects to this url after successfully logged out
    # does a reverse lookup for this string
    next_page = 'home'
