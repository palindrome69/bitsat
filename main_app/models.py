from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse,reverse_lazy
from django.utils import timezone

'''All models for this app are defined here.
   
   A django model class is basically a table in the database.
   For more information see
   https://docs.djangoproject.com/en/2.1/topics/db/models/

   user model used for this website is the django's in-built User model

   For more information on User see:
   https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User


'''

class Profile(models.Model):

    '''Profile of a user.

       Every User model object created has a corresponding
       Profile object. Profile has some more information about
       the user.

       '''
    USER_TYPES =   [('aspirant', 'Aspirant'), ('student', 'Student')]

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_type = models.TextField(blank = False, choices = USER_TYPES)
    bio = models.CharField(max_length = 250, blank = True)

    @property  # decorator
    def full_name(self):
        '''returns the user's full name
        '''
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    '''Questions asked by different Users.
       
    '''
    question = models.TextField(blank=False,)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name='questions')
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

    validity = models.IntegerField(default = 0, blank = False)

    def __str__(self):
        return self.answer

class Notification(models.Model):
    '''When a new answer is created the author of the question
       and users following the question
       will be notified by creating a new notification object.
    '''

    # whom to notify. (Profile object)
    to = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'notifications')

    # whose action caused the notification (Profile object)
    by = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'actions')

    # answer which caused notification
    answer = models.ForeignKey(Answer, on_delete = models.CASCADE, related_name = 'actions')
    
    date = models.DateTimeField(blank=False)

    # boolean field which is true if notification is viewed.
    viewed = models.BooleanField(default = False)

    def __str__(self):
        return self.by.user.username + " to " + self.to.user.username

    @classmethod
    def create_notif(cls, question, answer, profile):
        '''Creates notif for the author and users following the question
           when someone other than the author of the question posts the
           answer to the question

           question : Question which was answered.
           answer   : answer which led to notification.
           profile  : profile object of the logged in user.

        '''
        following_users = question.following.all()
        author = question.author

        # prevents creating notification if author of the question
        # posts an answer to the question
        if author != profile:
            author_notif = cls(to = author, by = profile,
                                        answer = answer, date = timezone.now())
            author_notif.save()
        else:
            pass    
        # creates notifs for users following the question
        for user in following_users:
            if user != profile and user != author:
                followers_notif = cls(to = user, by = profile,
                                               answer = answer, date = timezone.now())
                followers_notif.save()
            else:
                pass    


class Vote(models.Model):
    '''Votes are given to question and it can be an Upvote
       or a Downvote. field 'user' is the profile of user which
       voted on a question 'question
    '''
    # List of tuple with type of votes
    VOTE_TYPES = [('Upvote', 'Upvote'), ('Downvote', 'Downvote')]

    type = models.CharField(max_length = 50, blank = False, choices = VOTE_TYPES)

    question = models.ForeignKey(Question,on_delete = models.CASCADE,
                                 related_name = 'votes', default = None)



    user = models.ForeignKey(Profile,on_delete = models.CASCADE,
                             related_name = 'votes')

    class Meta:
        '''Meta Classes helps adding metadata to the model.

           For more information on Meta see :
           https://docs.djangoproject.com/en/2.1/topics/db/models/#meta-options
        
        '''
        # Adds a unique constraint on the fields.
        unique_together = (('question','user', 'type'),)

    def __str__(self):
        return  self.type + " " + self.user.user.username

class VoteAns(models.Model):
    '''model for votes to an answer
    '''
    # List of tuple with type of votes
    VOTE_TYPES = [('Upvote', 'Upvote'), ('Downvote', 'Downvote')]

    type = models.CharField(max_length = 50, blank = False, choices = VOTE_TYPES)

    answer = models.ForeignKey(Answer,on_delete = models.CASCADE,
                                 related_name = 'votes', default = None)



    user = models.ForeignKey(Profile,on_delete =  models.CASCADE,
                             related_name = 'ans_votes')

    class Meta:
        '''Meta Classes helps adding metadata to the model.

           For more information on Meta see :
           https://docs.djangoproject.com/en/2.1/topics/db/models/#meta-options
        
        '''
        # Adds a unique constraint on the fields.
        unique_together = (('answer','user', 'type'),)
