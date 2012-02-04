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
from puzzlaef.puzzle.utils import fetch_user_puzzles
from puzzlaef.settings import STATIC_URL
from string import split


PAGES = ['Play', 'Discover', 'Help a Puzzlaef']
PAGES_FULL = PAGES + ['Settings', 'Logout']
PAGES_LOCATIONS = ['pageTemplates/play.html', 'pageTemplates/discover.html', 'pageTemplates/helpPuzzlaef.html', 'pageTemplates/profile.html', 'registration/logout.html']
	
def start(request):
	if request.user.is_authenticated():
	    # TODO: show profile
		form = UserProfileForm(data=request.POST)
		puzzles = fetch_user_puzzles(request.user)
		return render_to_response('pageTemplates/page_layout.html', {'pages': PAGES, 'current_page': PAGES_FULL[0], 'current_page_template': PAGES_LOCATIONS[0], 'puzzles': fetch_user_puzzles(request.user), 'empty': len(puzzles)==0 },  context_instance=RequestContext(request))
	else:
	    return HttpResponseRedirect('/accounts/login/')

@login_required
def show_profile(request):
	context = RequestContext(request)
#	for key, value in extra_context.items():
#		context[key] = callable(value) and value() or value
	form = UserProfileForm(data=request.POST)
	return render_to_response('pageTemplates/page_layout.html', RequestContext(request, {'form': form, 'pages': PAGES, 'current_page': 'Settings', 'current_page_template': PAGES_LOCATIONS[4] }))
	
@login_required
def get_profile_form(request):
	form = UserProfileForm(data=request.POST)
	return form

@csrf_protect
@login_required
def make_move(request):
	if request.method == 'POST':
		user = User.objects.get(id=request.user.id)
		puzzle_id = request.session["puzzle_id"]
		list = PuzzlePiece.objects.filter(puzzle=puzzle_id)
		puzzle_piece = list[len(list)-1]
		if(puzzle_piece == None):
			print '>>>>>>>>>>>>>>>> empty piece'
		photo = Photo(user = user, image = ImageFile(request.FILES['puzzlaefFile']))
		photo.save()
		if(puzzle_piece.puzzle.turn == puzzle_piece.puzzle.player1):
			puzzle_piece.photo1 = photo
		else:
			puzzle_piece.photo2 = photo
		puzzle_piece.save()
		
		send_mail('Puzzlaef - it is now your turn!', puzzle_piece.puzzle.title, EMAIL_HOST_USER, [user.email], fail_silently=False)
		
		if not puzzle_piece.photo1 or not puzzle_piece.photo2:	
			if(puzzle_piece.puzzle.turn == puzzle_piece.puzzle.player1):
				puzzle_piece.puzzle.turn = puzzle_piece.puzzle.player2
			else:
				puzzle_piece.puzzle.turn = puzzle_piece.puzzle.player1
			puzzle_piece.puzzle.save()
		else:
			if(puzzle_piece.puzzle.turn == puzzle_piece.puzzle.player1):
				new_piece = PuzzlePiece(puzzle=puzzle_piece.puzzle)
			else:
				new_piece = PuzzlePiece(puzzle=puzzle_piece.puzzle)
			new_piece.save()
		
		userTurn = puzzle_piece.puzzle.turn == request.user
		
		if not puzzle_piece.photo1 and not puzzle_piece.photo2:
			newTurn = True
		else:
			newTurn = False
		
		render = render_to_string("puzzle/puzzle.html", { 'puzzle': puzzle_piece.puzzle, 
														'pieces': pieces,
														'newTurn':newTurn, 
														'userTurn':userTurn, 
														'user': request.user}, context_instance=RequestContext(request))
														
		return HttpResponse(simplejson.dumps({"success":True, "newRender":render}))	
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
		
		pictureGrid = PictureGrid(getThemes()).getGridAsString();
		render = render_to_string("puzzle/pickTheme.html", {"startWith":username, 'pictureGrid': pictureGrid}, context_instance=RequestContext(request))
		
		return HttpResponse(simplejson.dumps({"success":True, "newRender":render}))	
	else:
		return HttpResponse(simplejson.dumps({"error":"Method not POST"}))	
	
