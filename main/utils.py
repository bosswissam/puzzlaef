'''
Created on Jan 30, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from django.db import models
from django.contrib.auth.models import User
 
class ResultUser(object):
    username = models.CharField()
    first_name = models.CharField()
    last_name = models.CharField()
    location = models.CharField()
    
    def __init__(self, user_profile):
        print 'biatch', user_profile.user.username
        self.username = user_profile.user.username
        self.first_name = user_profile.user.first_name
        self.last_name = user_profile.user.last_name
        self.location = user_profile.location