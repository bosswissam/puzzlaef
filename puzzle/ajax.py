from puzzlaef.forms import UserProfileForm
from puzzlaef.main.models import UserProfile
from django.contrib.auth.decorators import login_required
from puzzlaef.puzzle.models import Puzzle
from puzzlaef.puzzle.models import PuzzlePiece
from puzzlaef.puzzle.utils import *
from puzzlaef.views import PAGES, PAGES_LOCATIONS
from puzzlaef.dajax.core import Dajax
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

@dajaxice_register
def get_start_puzzle_content(request):
	openPuzzlePieces = fetch_all_open_puzzle_pieces(request.user)
	
	render = render_to_string("puzzle/startPuzzleContent.html", {"openPuzzlePieces":openPuzzlePieces}, 
																context_instance=RequestContext(request))
	dajax = Dajax()
	dajax.assign('#start-puzzle-panel', 'innerHTML', render)
	dajax.script(render_to_string("puzzle/uploadButton.html", {"style":"", "id":"start-puzzle-file-uploader", "label":"Upload a new photo for a new Puzzle", "action":"upload/newPuzzle", "onCompleteCallback":"onComplete: new_puzzle_started,"}));

	dajax.script("initialize_start_puzzle()")
	return dajax.json()

@login_required
@dajaxice_register
def join_play_puzzle(request, puzzle):
    
	joined_puzzle = join_puzzle(request.user, puzzle)
	
	printer = PuzzlePrinter()
	puzzleAsString = printer.get_user_puzzle_as_string(joined_puzzle, request)
	
	#TODO: The uploadbuttonscript is probably not needed here!
	uploadButtonScript = render_to_string("puzzle/uploadButton.html", 
							{"style":"float:none; width: 70px; margin-left: auto; margin-right: auto; padding: 10px", 
							"id":"plus-button", 
							"label":"Add Picture", 
							"action":"upload/theme", 
							"onCompleteCallback":"onComplete: refreshPuzzle,"})
	return simplejson.dumps({'puzzleAsString': puzzleAsString, 'uploadButtonScript': uploadButtonScript})

@login_required
@dajaxice_register
def get_profile(request):
		userProfileObj = get_user_profile(request.user)
		form = UserProfileForm(initial={'first_name': userProfileObj.user.first_name, 'last_name': userProfileObj.user.last_name, 'location':userProfileObj.location})
		profile = render_to_string('pageTemplates/profile.html', RequestContext(request, {'form': form}))
		return simplejson.dumps({'profile': profile})


@dajaxice_register
def open_puzzle(request, puzzle):
	request.session["puzzle_id"] = puzzle
	return get_latest_puzzle(request)

@dajaxice_register
@login_required
def get_latest_puzzle(request, puzzle_id):
	printer = PuzzlePrinter()
	puzzleAsString = printer.get_user_puzzle_as_string(get_puzzle(puzzle_id), request)

@dajaxice_register
def needs_help(request, puzzle_piece):
    puzzle = PuzzlePiece(id=puzzle_piece)
    puzzle.needs_help = True
    puzzle.save()
    pass
