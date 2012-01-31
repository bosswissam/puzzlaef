'''
Created on Jan 29, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from django import forms

class UserProfileForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(), max_length = 30)
    last_name = forms.CharField(required=False, widget=forms.TextInput(), max_length = 30)
    avatar = forms.ImageField(required=False)
    location = forms.CharField(required=False, widget=forms.TextInput(), max_length = 100)
    
    def __init__(self, data=None, remoteip=None, *args, **kwargs):
        super(UserProfileForm, self).__init__(data=data, *args, **kwargs)
