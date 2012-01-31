from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from puzzlaef.forms import UserProfileForm
from django.core.files.images import ImageFile
from django.views.decorators.csrf import csrf_protect
from puzzlaef.forms import UserProfileForm
from puzzlaef.main.ajax import fetch_user_puzzles
from puzzlaef.main.models import UserProfile
from puzzlaef.puzzle.models import Photo
from django.contrib.auth.models import User


PAGES = ['Play', 'Discover', 'Help a Puzzlaef']
PAGES_FULL = PAGES + ['Settings', 'Logout']
PAGES_LOCATIONS = ['pageTemplates/play.html', 'pageTemplates/discover.html', 'pageTemplates/helpPuzzlaef.html', 'pageTemplates/profile.html', 'registration/logout.html']

def start(request):
	if request.user.is_authenticated():
	    # TODO: show profile
		form = UserProfileForm(data=request.POST)
		return render_to_response('pageTemplates/page_layout.html', RequestContext(request, {'pages': PAGES, 'current_page': PAGES_FULL[0], 'current_page_template': PAGES_LOCATIONS[0], 'puzzles': fetch_user_puzzles(request) }))
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

@login_required
def make_move(request):
	if request.method == 'POST':
		form = PuzzlePieceForm(request.POST, request.FILES)
		if form.is_valid():
			puzzle_piece = puzzle_piece.objects.get(user=request.user.id)
			if(puzzle_piece == None):
				puzzle_piece = PuzzlePiece()
			if(puzzle_piece.puzzle.player1==request.user.id):
				x = request.user
				puzzle_piece.photo1 = request.FILES['photo1']
			else:
				x = puzzle_piece.puzzle.player2
				puzzle_piece.photo2 = request.FILES['photo2']
		puzzle_piece.save()
		if(puzzle_piece.puzzle.turn == request.user.id):
			puzzle_piece.puzzle.turn = puzzle_piece.puzzle.player2
		else:
			puzzle_piece.puzzle.turn = request.user.id
		send_mail('Puzzlaef - it is now your turn!', puzzle_piece.puzzle.title, EMAIL_HOST_USER, x.email, fail_silently=False)
	else:
		form = PuzzlePieceForm()
		

@csrf_protect
@login_required
def upload_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user_profile = UserProfile.objects.get(user=request.user.id)
		user_profile.avatar = ImageFile(request.FILES['avatar'])
		user_profile.save()
	else:
		form = UserProfileForm()
	pass

@csrf_protect
@login_required
def upload_theme(request):
	if request.method == 'POST':
		theme = ImageFile(request.FILES['new_theme'])
		photo = Photo()
		photo.image = theme
		photo.user = User.objects.get(id=request.user.id)
		photo.isTheme = True
		print photo
		photo.save()
	else:
		form = UserProfileForm()
	pass
