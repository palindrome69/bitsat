from django import template
from main_app.models import Question, Profile, Vote

'''All custom filters are defined here.
   
    usage of filters in a template :
    if the filter is:

    def fiter(value, arg):
        # code

    In template it will be used as:

        {{ value|filter:arg }}

   '''
# new instance of library. Registers the filters and tags
register = template.Library()

@register.filter(name='vote_count')  # decorator
def vote_count(question):
    ''' returns the number of upvotes and
        downvotes for the question as a string
    
    '''
    upvotes, downvotes = 0, 0
    upvotes = sum(1 for vote in question.votes.all() if vote.type == 'Upvote')
    downvotes = sum(1 for vote in question.votes.all() if vote.type == 'Downvote')

    return "{} Up Votes , {} Down Votes ".format(upvotes, downvotes)

@register.filter(name='check_voted')   #decorator
def check_voted(question, user):
    '''checks if the user
       has voted on this question or not
    
    '''
    flag = 0
    for vote in question.votes.all():
        if vote.user.user == user:
            flag = vote.type
            break
    return flag

@register.filter(name='opp_vote')
def opp_vote(question, user):
    '''returns the opposite of the vote
       by the user on the question.

    '''
    profile = user.profile
    vote = question.votes.filter(user = profile)[0]
    if vote.type == "Upvote":
        return "Downvote"
    else :
        return "Upvote"

@register.filter(name = 'upvoted_questions')
def upvoted_questions(user):
    '''returns list of questions upvoted
       by the user.

    '''   
    profile = user.profile
    questions = []
    votes = Vote.objects.filter(user = profile, type = 'Upvote',)
    for vote in votes:
        if vote.question != None:
            questions.append(vote.question)
    return questions

@register.filter(name = 'following_questions')
def following_questions(user):
    '''returns queryset of questions
       followed by the user

    '''    
    profile = user.profile
    return profile.following.all()

@register.filter(name = 'check_following')
def check_following(question, user):
    '''returns 1 if user follows the
       question else returns 0

    '''
    profile = user.profile
    flag = 0
    for followers in question.following.all():
        if profile == followers:
            flag = 1
            break
    return flag

@register.filter(name = 'is_viewed')
def is_viewed(notifs):
    '''returns the list of notifications
       which are not viewed from notifs.

    '''   
    viewed_notifs = []
    for notif in notifs:
        if notif.viewed == False:
            viewed_notifs.append(notif)

    # brings most recent at first        
    viewed_notifs.reverse()

    return viewed_notifs

@register.filter(name = 'order_by_votes')
def order_by_votes(answers):
    '''returns answers by decreasing
       order of valididty
    '''
    return answers.order_by('-validity')

@register.filter(name = 'top_voted')
def top_voted(answers):
    '''returns answer with highest validity'''
    if answers:
        sorted_ans = order_by_votes(answers)
        return sorted_ans[0]
    else :
        return "***NO ANSWERS***"    

@register.filter('top_three')
def top_three(answers):
    if len(answers)>3:
        return answers[:3]
    else:
        return answers        
