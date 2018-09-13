from django.contrib import admin
from .models import *

'''Registers the models to the admin site.
   Go to 'domain.com/admin' to see them.
'''

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Notification)
