'''
Created on Jan 30, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from puzzlaef.forms import UserProfileForm
from puzzlaef.main.models import UserProfile
from puzzlaef.puzzle.models import Puzzle
from puzzlaef.views import PAGES, PAGES_LOCATIONS
from puzzlaef.dajax.core import Dajax
from puzzlaef.dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.core import serializers
from django.template.loader import render_to_string

@dajaxice_register
def fetch_user_puzzles(request):
    list = Puzzle.objects.get(user=request.id)
    dajax = Dajax()
    dajax.assign('#user-puzzles', 'innerHTML', {})
    return dajax.json()

@dajaxice_register
def fetch_themes(request):
    list = Puzzle.objects.all()
    dajax = Dajax()
    dajax.assign('#all-puzzle-themes', 'innerHTML', {})
    return dajax.json()