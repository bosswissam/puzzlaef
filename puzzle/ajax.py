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
from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext

@dajaxice_register
def fetch_discover(request):
   list = Puzzle.objects.all()
   results = [x._dict_ for x in list]
   return simplejson.dumps(result)	


fakePictureURL = "http://www.blogcdn.com/www.engadget.com/media/2012/01/2012-01-29-sony200_216x150.jpg"
fakePictureTitle = "Great Sunset"
fakePictureSet = [PictureThumb(fakePictureURL,fakePictureURL,fakePictureTitle) for i in range(15)]


@dajaxice_register
def start_puzzle(request, username):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess
    
	pictureGrid = PictureGrid(getThemes()).getGridAsString();
    
	render = render_to_string("puzzle/pickTheme.html", {"startWith":username, 'pictureGrid': pictureGrid}, context_instance=RequestContext(request))
	dajax = Dajax()
	dajax.assign('#page-container', 'innerHTML', render)
	dajax.script(render_to_string("puzzle/uploadButton.html", {"style":"float:none; width: 200px; margin-left: auto; margin-right: auto; padding: 20px; font-size:15px", "id":"file-uploader", "label":"Upload your Own Theme", "action":"upload/theme", "onCompleteCallback":"onComplete: refreshThemes,"}));
	dajax.script("initialize_pick_theme('"+ username +"')")
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
def theme_picked(request, opponent, theme):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess
	username = request.user.username
	
	puzzle_id = make_new_puzzle(request.user, opponent)
	request.session["puzzle_id"] = puzzle_id
	
	set_puzzle_theme(request, puzzle_id, theme)
	return get_latest_puzzle(request)

@dajaxice_register
def get_latest_picture_grid(request):
	pictureGrid = PictureGrid(getThemes()).getGridAsString();
	return simplejson.dumps({'newPictureGrid':pictureGrid})


@dajaxice_register
def open_puzzle(request, puzzle):
	request.session["puzzle_id"] = puzzle
	return get_latest_puzzle(request)

@dajaxice_register
def get_latest_puzzle(request):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess
	username = request.user.username
	
	puzzle_id = request.session["puzzle_id"]
	pieces = get_puzzle_pieces(puzzle_id)
	latest_puzzle_piece = pieces[len(pieces)-1]
	userTurn = latest_puzzle_piece.puzzle.turn == request.user
	
	if request.user == latest_puzzle_piece.puzzle.player1:
		opponent = latest_puzzle_piece.puzzle.player2
	else:
		opponent = latest_puzzle_piece.puzzle.player1
	
	if latest_puzzle_piece.photo1 is None and latest_puzzle_piece.photo2 is None:
		newTurn = True
	else:
		newTurn = False
		
	render = render_to_string("puzzle/puzzle.html", { 'puzzle': get_puzzle(puzzle_id), 'pieces': pieces, 'newTurn':newTurn, 'userTurn':userTurn, 'user': request.user, 'opponent': opponent}, context_instance=RequestContext(request))
	dajax = Dajax()
	dajax.assign('#page-container', 'innerHTML', render)
	dajax.script(render_to_string("puzzle/uploadButton.html", {"style":"float:none; font-size:50px", "id":"plus-button", "label":"+", "action":"upload/makeMove", "onCompleteCallback":"onComplete: refreshPuzzle,"}));
	return dajax.json()

@dajaxice_register
def needs_help(request, puzzle_piece):
    puz = PuzzlePiece(id=puzzle_piece)
    puz.needs_help = True
    puz.save()
    pass
