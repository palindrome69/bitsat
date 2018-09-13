from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate

'''All the forms required in the website.
   Instance of each class is a new django form.
'''

class UserForm(UserCreationForm):

    class Meta:
        ''' Meta helps adding metadata to the form class.
            Basically data which is not a field.
        '''
        model = User

        # Fields which must be used in the form
        fields = ('username', 'email','first_name',
                  'last_name','password1', 'password2')

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget = forms.PasswordInput())
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    ''' Form class which focuses on the profile
        components of a user like the bio and user_type
    '''

    class Meta:
        ''' Meta helps adding metadata to the form class.
            Basically data which is not a field.
        '''
        model = Profile

        # Fields which must be used in the form
        fields = ('user_type','bio')

    # overrides __init__ method to customize widgets
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # sets label to fields
        self.fields['user_type'].label = 'What are you'
        self.fields['bio'].label = 'Write Something about Yourself'

        # sets help text to 'bio' field
        self.fields['bio'].help_text = '''It is advised to mention your desired
                                          branch and score If you're an aspirant'''


class QuestionForm(forms.ModelForm):

    class Meta:
        ''' Meta helps adding metadata to the form class.
            Basically data which is not a field.
        '''
        model = Question

        # Fields which must be used in the form
        fields = ('question' ,)

        # Customizing widgets
        widgets = {
            'question': forms.Textarea(attrs={'rows': 2}),
        }

    # overrides __init__ method to customize widgets
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # sets the label of question field
        self.fields['question'].label = ''
