from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate

'''All the forms required in the website.
   Instance of each class is a new django form.

   For more information see :
   https://docs.djangoproject.com/en/2.1/topics/forms/

'''

class UserForm(UserCreationForm):

    class Meta:
        ''' Meta helps adding metadata to the form class.
        '''
        # form will be made for this model class
        model = User

        # Fields which must be used in the form
        fields = ('username', 'email','first_name',
                  'last_name','password1', 'password2')

class PasswordChangeForm(forms.Form):
    '''Form for changing password of the user
    '''
    current_password = forms.CharField(widget = forms.PasswordInput())
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # customizations to the fields
        self.fields['password1'].label = 'New Password'
        self.fields['password1'].help_text = """Enter a strong password having
                                                 a combination of alphanumeric 
                                                 characters and special characters"""
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = 'Re-enter new Password'

class ProfileForm(forms.ModelForm):
    ''' Form class which focuses on the profile
        components of a user like the bio and user_type
    '''

    class Meta:
        model = Profile
        fields = ('user_type','bio')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['user_type'].label = 'What are you'
        self.fields['bio'].label = 'Write Something about Yourself'
        self.fields['bio'].help_text = '''It is advised to mention your desired
                                          branch and score If you're an aspirant'''


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question' ,)

        # Customizing widgets
        widgets = {
            'question': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['question'].label = ''
