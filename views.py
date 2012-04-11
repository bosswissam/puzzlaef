from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from puzzlaef.settings import EMAIL_HOST_USER
from puzzlaef.forms import UserProfileForm, UserProfileForm
from puzzlaef.main.models import UserProfile
from puzzlaef.puzzle.models import Puzzle, Photo, PuzzlePiece
from puzzlaef.puzzle.utils import *
from puzzlaef.settings import STATIC_URL
from string import split
from django.core import serializers

PAGES = ['Play']
PAGES_FULL = PAGES + ['Profile', 'Logout']
PAGES_LOCATIONS = ['pageTemplates/play.html', 'pageTemplates/profile.html', 'registration/logout.html']
		
		
def start(request):
	return show_play(request)
	
@login_required
def show_play(request):
	# TODO: show profile
	printer = PuzzlePrinter()
	userPuzzles = fetch_latest_user_puzzles(request.user)
	if len(userPuzzles) > 0:
		userPuzzleAsStrings = [printer.get_user_puzzle_as_string(puzzle, request) for puzzle in userPuzzles]
	else:
		userPuzzleAsStrings = None
	print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", userPuzzleAsStrings
	nonUserPuzzles = fetch_latest_nonuser_puzzles(request.user)
	nonUserPuzzlesAsStrings = [printer.get_foreign_puzzle_as_string(puzzle) for puzzle in nonUserPuzzles]
	return render_to_response('pageTemplates/page_layout.html', {'pages': PAGES, 'current_page': PAGES_FULL[0], 
																'current_page_template': PAGES_LOCATIONS[0], 
																'latest_user_puzzles': userPuzzleAsStrings,
																'latest_other_puzzles': nonUserPuzzlesAsStrings,
																'user': request.user},  
																context_instance=RequestContext(request))

@login_required
def show_profile(request):
	context = RequestContext(request)
#	for key, value in extra_context.items():
#		context[key] = callable(value) and value() or value
	form = UserProfileForm(data=request.POST)
	return render_to_response('pageTemplates/page_layout.html', RequestContext(request, {'form': form, 'pages': PAGES, 'current_page': PAGES_FULL[1], 'current_page_template': PAGES_LOCATIONS[1] }))
	
@login_required
def get_profile_form(request):
	form = UserProfileForm(data=request.POST)
	return form

@csrf_protect
@login_required
def new_puzzle(request):
	if request.method == 'POST':
		user = request.user
		photo = Photo(user = user, image = ImageFile(request.FILES['puzzlaefFile']))
		photo.save()
		make_new_puzzle(user, photo)
		return HttpResponse(simplejson.dumps({"success":True}), mimetype='application/javascript')	
	else:
		return HttpResponse(simplejson.dumps({"error":"Method not POST"}))
			
@csrf_protect
@login_required
def make_move(request):
	if request.method == 'POST':
		user = request.user
		puzzle_id = long(request.GET['puzzle'])
		puzzle = get_puzzle(puzzle_id)
		photo = Photo(user = user, image = ImageFile(request.FILES['puzzlaefFile']))
		photo.save()
		
		move_made = make_move_with_photo(user, puzzle_id, photo)
		
		if move_made:
			send_mail('Puzzlaef - it is now your turn!', "It's your turn to respond in the puzzle " + str(puzzle), EMAIL_HOST_USER, [user.email], fail_silently=False)	
			
			printer = PuzzlePrinter()
			puzzleAsString = printer.get_user_puzzle_as_string(get_puzzle(puzzle_id), request)											
			return HttpResponse(simplejson.dumps({"success":True, "puzzleAsString":puzzleAsString, "puzzleID": request.GET['puzzle']}), mimetype='application/javascript')	
		else:
			return HttpResponse(simplejson.dumps({"error":"It is not your turn or you do not have access to this puzzle"}))	
	else:
		return HttpResponse(simplejson.dumps({"error":"Method not POST"}))	
		

@csrf_protect
@login_required
def upload_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user_profile = UserProfile.objects.get(user=request.user.id)
		user_profile.avatar = ImageFile(request.FILES['puzzlaefFile'])
		user_profile.save()
		return HttpResponse(simplejson.dumps({"success":True}))	
	else:
		form = UserProfileForm()
		return HttpResponse(simplejson.dumps({"error":"Method not POST"}))
	

@csrf_protect
@login_required
def upload_theme(request):
	if request.method == 'POST':
		theme = ImageFile(request.FILES['puzzlaefFile'])
		photo = Photo()
		photo.image = theme
		photo.user = User.objects.get(id=request.user.id)
		photo.title = split(theme.name, '.')[0]
		photo.isTheme = True
		photo.save()

		return HttpResponse(simplejson.dumps({"success":True}))	
	else:
		return HttpResponse(simplejson.dumps({"error":"Method not POST"}))	
	
