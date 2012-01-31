'''
Created on Jan 30, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from puzzlaef.forms import UserProfileForm
from puzzlaef.main.models import UserProfile
from puzzlaef.main.ajax import assert_access
from puzzlaef.puzzle.models import Puzzle
from puzzlaef.puzzle.models import PuzzlePiece
from puzzlaef.puzzle.utils import *
from puzzlaef.views import PAGES, PAGES_LOCATIONS
from puzzlaef.dajax.core import Dajax
from puzzlaef.puzzle.utils import PictureGrid, PictureThumb
from puzzlaef.dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.core import serializers
from django.template.loader import render_to_string

fakePictureURL = "http://www.blogcdn.com/www.engadget.com/media/2012/01/2012-01-29-sony200_216x150.jpg"
fakePictureTitle = "Great Sunset"
fakePictureSet = [PictureThumb(fakePictureURL,fakePictureURL,fakePictureTitle) for i in range(15)]

@dajaxice_register
def fetch_discover(request):
   list = Puzzle.objects.all()
   results = [x._dict_ for x in list]
   return simplejson.dumps(result)

@dajaxice_register
def fetch_themes(request):
    list = Puzzle.objects.all()
    dajax = Dajax()
    dajax.assign('#all-puzzle-themes', 'innerHTML', {})
    return dajax.json()


fakePictureURL = "http://www.blogcdn.com/www.engadget.com/media/2012/01/2012-01-29-sony200_216x150.jpg"
fakePictureTitle = "Great Sunset"
fakePictureSet = [PictureThumb(fakePictureURL,fakePictureURL,fakePictureTitle) for i in range(15)]


@dajaxice_register
def start_puzzle(request, username):
    assertAccess = assert_access(request.user)
    if(assertAccess):
        return assertAccess
    
    puzzle_id = make_new_puzzle(request.user, username)
    
    pictureGrid = PictureGrid(fakePictureSet).getGridAsString();
    
    render = render_to_string("puzzle/pickTheme.html", {"startWith":username, 'pictureGrid': pictureGrid})
    dajax = Dajax()
    dajax.assign('#page-container', 'innerHTML', render)
    dajax.script("initialize_pick_theme('"+ str(puzzle_id) +"')")
    return dajax.json()

class Piece():
	def __init__(self, piece1, piece2, user1, user2):
		self.photo1 = piece1
		self.photo2 = piece2
		self.user1 = user1
		self.user2 = user2

photo1 = "http://www.blogcdn.com/www.engadget.com/media/2012/01/attgalaxynoteltelead_216x150.jpg"
photo2 = "http://www.blogcdn.com/www.engadget.com/media/2012/01/rim-be-bold2.jpg"
user1 = "sinchan"
user2 = "wissam"
pieces = [Piece(photo1,photo2, user1, user2) for i in range(10)]

@dajaxice_register
def theme_picked(request, puzzle, theme):
    assertAccess = assert_access(request.user)
    if(assertAccess):
        return assertAccess
        
    set_puzzle_theme(puzzle, theme)
    render = render_to_string("puzzle/puzzle.html", { 'pieces': pieces, 'newTurn':True, 'userTurn':True, 'user': 'sinchan' })
    dajax = Dajax()
    dajax.assign('#page-container', 'innerHTML', render)
    #dajax.script("initialize_pick_theme('"+ puzzle_id +"')")
    return dajax.json()

@dajaxice_register
def fetch_discover(request):
    list = Puzzle.objects.all()
    results = [x.__dict__ for x in list]
    return simplejson.dumps(result)

@dajaxice_register
def get_photos(request):
    assertAccess = assert_access(request.user)
    if(assertAccess):
        return assertAccess
    
    list = Photos.objects.get(user=request.user)
    
    pictureGrid = PictureGrid(fakePictureSet).getGridAsString();
    
    render = render_to_string("puzzle/profile.html", {'pictureGrid': pictureGrid})
    dajax = Dajax()
    dajax.assign('#page-container', 'innerHTML', render)
    return dajax.json()