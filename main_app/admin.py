from django.contrib import admin
from .models import *

'''Any customizations to the admin site are done here

   For more info:
   https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
   
'''
# registers the model in the admin site.
# visit domain.com/admin to see the admin page 
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Notification)
admin.site.register(VoteAns)
