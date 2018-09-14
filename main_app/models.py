from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from django.utils import timezone


class Profile(models.Model):

    '''Profile of a user.
       This extends the functionality of the built in User model by
       giving it a profile through a OneToOneField.
       the user attribute is the user whose profile is defined .
       '''

    # list of tuples where first element of tuple is actual
    # value of the type and second is the human readable value of it.
    USER_TYPES =   [('aspirant', 'Aspirant'), ('student', 'Student')]

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_type = models.TextField(blank = False, choices = USER_TYPES)
    bio = models.CharField(max_length = 250, blank = True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    '''Questions asked by different Users.
       'author' is the Profile of the user which asked the question.
    '''
    question = models.TextField(blank=False,)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name='questions')
    # Date when question published.
    pub_date = models.DateTimeField(blank = False)

    # Users which are following this question.
    following = models.ManyToManyField(Profile,related_name = 'following')

    # This is basically the difference of upvotes and downvotes to the question.
    validity = models.IntegerField(default = 0, blank = False)

    def __str__(self):
        return self.question

class Answer(models.Model):
    '''Answers by different Users.
      'author' is the Profile of the user answered the
       Question 'question'.
    '''
    answer = models.TextField(blank = False)
    question = models.ForeignKey(Question, on_delete = models.CASCADE,
                                 default = None, related_name='answers')
    author = models.ForeignKey(Profile, on_delete = models.CASCADE,
                               related_name = 'answers')
    # Date when answered.
    pub_date = models.DateTimeField(blank=False)

    def __str__(self):
        return self.answer

class Notification(models.Model):
    '''When a new answer is created the author of the question
       and users  following the question
       will be notified by creating a new notification object.
    '''

    # whom to notify
    to = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'notifications')

    # whose action caused the notification
    by = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'actions')

    # answer which caused notification
    answer = models.ForeignKey(Answer, on_delete = models.CASCADE, related_name = 'actions')
    
    date = models.DateTimeField(blank=False)

    # checks if notification is viewed
    viewed = models.BooleanField(default = False)

    def __str__(self):
        return self.by.user.username + " to " + self.to.user.username


class Vote(models.Model):
    '''Votes are given to question and it can be an Upvote
       or a Downvote. field 'user' is the profile of user which
       voted on a question 'question
    '''
    # List of tuple with type of votes
    VOTE_TYPES = [('Upvote', 'Upvote'), ('Downvote', 'Downvote')]

    type = models.CharField(max_length = 50, blank = False, choices = VOTE_TYPES)

    question = models.ForeignKey(Question,on_delete = models.CASCADE,
                                 related_name = 'votes')
    user = models.ForeignKey(Profile, models.CASCADE,
                             related_name = 'votes')

    class Meta:
        '''Meta Classes provide more funtionality to a Model.

           For more information on Meta see :
           https://docs.djangoproject.com/en/2.1/topics/db/models/#meta-options
        
        '''
        # Adds a unique constraint on the fields.
        unique_together = (('question','user', 'type'),)

    def __str__(self):
        return  self.type + " " + self.user.user.username
