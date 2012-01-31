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

@dajaxice_register
def start_puzzle(request, username):
    assertAccess = assert_access(request.user)
    if(assertAccess):
        return assertAccess
    
    puzzle_id = make_new_puzzle(username)
    
    pictureGrid = PictureGrid(fakePictureSet).getGridAsString();
    
    render = render_to_string("puzzle/pickTheme.html", {"startWith":username, 'themes': getThemes(), 'pictureGrid': pictureGrid})
    dajax = Dajax()
    dajax.assign('#page-container', 'innerHTML', render)
    dajax.script("initialize_pick_theme('"+ puzzle_id +"')")
    return dajax.json()


@dajaxice_register
def theme_picked(request, puzzle, theme):
    assertAccess = assert_access(request.user)
    if(assertAccess):
        return assertAccess
        
    set_puzzle_theme(puzzle, theme)
    render = render_to_string("puzzle/puzzle.html", { 'puzzle': get_puzzle(puzzle) })
    dajax = Dajax()
    #dajax.assign('#page-container', 'innerHTML', render)
    #dajax.script("initialize_pick_theme('"+ puzzle_id +"')")
    return dajax.json()