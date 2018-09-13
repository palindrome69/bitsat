from django import template
from main_app.models import Question, Profile, Vote

'''All custom filters are defined here.
   A new instance of Library registers the filters
   for use in HTML files.
   '''

register = template.Library()

@register.filter(name='vote_count')  # decorator
def vote_count(value):
    ''' returns the number of upvotes and
        downvotes for the question
        PARAMETER
            value : question whose number of votes is required
    '''
    upvotes, downvotes = 0, 0
    for vote in value.votes.all():
        if vote.type == "Upvote":
            upvotes += 1
        elif vote.type == 'Downvote':
            downvotes += 1
    return "{} Up Votes , {} Down Votes ".format(upvotes, downvotes)

@register.filter(name='check_voted')   #decorator
def check_voted(value, arg):

    '''checks if the logged in user
       has voted on this question or not
       PARAMETERS
                value : question which is checked
                arg   : user logged in
    '''
    flag = 0
    for vote in value.votes.all():
        if vote.user.user == arg:
            flag = vote.type
            break
    return flag

@register.filter(name='opp_vote')
def opp_vote(value, arg):

    '''returns the opposite of the vote
       if question is voted by the logged in user
       PARAMETERS
                value : question object in use
                arg   : logged in user
    '''
    profile = Profile.objects.filter(user = arg)[0]
    vote = value.votes.filter(user = profile)[0]
    if vote.type == "Upvote":
        return "Downvote"
    else :
        return "Upvote"

@register.filter(name = 'first_answer')
def first_answer(value):
    '''returns the first answer to the question if there is any
        PARAMETER
                value : question whose first answer is required
    '''
    if value.answers.all():
        ans = value.answers.all()[0].answer
        return ans
    else:
        return "***No Answers Yet***"

@register.filter(name = 'upvoted_questions')
def upvoted_questions(value, arg):
    profile = Profile.objects.filter(user = arg)[0]
    votes = Vote.objects.filter(user = profile, type = 'Upvote')
    questions = [vote.question for vote in votes]
    return questions

@register.filter(name = 'following_questions')
def following_questions(value, arg):
    profile = Profile.objects.filter(user = arg)[0]
    return profile.following.all()

@register.filter(name = 'order_by_votes')
def order_by_votes(value):

    return Question.objects.order_by('-validity')

@register.filter(name = 'check_following')
def check_following(value, arg):
    profile = Profile.objects.filter(user = arg)[0]
    flag = 0
    for followers in value.following.all():
        if profile == followers:
            flag = 1
            break
    return flag

@register.filter(name = 'is_viewed')
def is_viewed(value):
    viewed_notifs = []
    for notif in value:
        if notif.viewed == False:
            viewed_notifs.append(notif)
    viewed_notifs.reverse()        
    return viewed_notifs
