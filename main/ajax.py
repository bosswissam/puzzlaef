'''
Created on Jan 29, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from puzzlaef.forms import UserProfileForm
from puzzlaef.main.models import UserProfile
from puzzlaef.main.utils import ResultUser, ResultPiece
from puzzlaef.main.pictureGrid import PictureGrid
from puzzlaef.main.pictureThumb import PictureThumb
from puzzlaef.puzzle.models import Puzzle, Photo, PuzzlePiece
from puzzlaef.dajax.core import Dajax
from puzzlaef.dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.core import serializers
from django.template.loader import render_to_string
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from puzzlaef.views import *

import string

def assert_access(user):
	if user.is_authenticated():
		return None
	else:
		dajax = Dajax()
	 	dajax.redirect("/accounts/login",delay=0) 
		return dajax.json()

def get_pieces(request, puzzle):
	list = Puzzle.objects.filter(id=puzzle)
	result = [PuzzlePiece.objects.filter(puzzle=x.id) for x in list]
	return result

def fetch_user_puzzles(request):
	list1 = set(Puzzle.objects.filter(player1=request.user))
	list2 = set(Puzzle.objects.filter(player2=request.user))
	result = list(list1.union(list2))
	puzzle_pieces1 = [PuzzlePiece.objects.filter(puzzle=x) for x in result]
	puzzle_pieces = [x for x in puzzle_pieces1 if not len(x)==0]
	final = [ResultPiece(result[x].id,
						puzzle_pieces[x].photo1, 
						puzzle_pieces[x].photo2,
						result[x].player1.username,
						result[x].player2.username,
						UserProfile.objects.get(user=result[x].player1).location,
						UserProfile.objects.get(user=result[x].player2).location) for x in range(len(puzzle_pieces))]
	if len(final)==0:
		final = [ResultPiece(result[x].id, None, None,
							result[x].player1.username,
							result[x].player2.username,
							UserProfile.objects.get(user=result[x].player1).location,
							UserProfile.objects.get(user=result[x].player2).location) for x in range(len(result))]
	return final

@dajaxice_register
def send_form(request, form):
    dajax = Dajax()
    form = UserProfileForm(form)
    if form.is_valid():
        user_profile = UserProfile.objects.get(user=request.user.id)
        user = User.objects.get(id = request.user.id)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user_profile.avatar = form.cleaned_data['avatar']
        user_profile.location = form.cleaned_data['location']
        user.save()
        user_profile.save()
        dajax.remove_css_class('#my_form input', 'error')
    else:
		dajax.remove_css_class('#my_form input', 'error')
		for error in form.errors:
			dajax.add_css_class('#id_%s' % error, 'error')
    return dajax.json()

@dajaxice_register
def open_puzzle(request, puzzle):
	render = render_to_string("puzzle/puzzle.html", { 'pieces': get_pieces(request, puzzle), 'newTurn':True, 'userTurn':True, 'user': 'sinchan' }, context_instance=RequestContext(request))
	dajax = Dajax()
	dajax.assign('#page-container', 'innerHTML', render)
	dajax.script("$('.fileUpload').fileUploader();")
	return dajax.json()

@dajaxice_register
def changePage(request, newPage):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess
	
	dajax = Dajax()
	if (newPage == PAGES_FULL[0]):
		template = PAGES_LOCATIONS[0]
		#print fetch_user_puzzles(request)
		render = render_to_string(template, {'puzzles': fetch_user_puzzles(request), 'empty': []})
		
	elif (newPage == PAGES_FULL[1]):
		template = PAGES_LOCATIONS[1]
		list = Puzzle.objects.all()
		render = render_to_string(template, {'list':list}, context_instance=RequestContext(request))
		
	elif (newPage == PAGES_FULL[2]):
		template = PAGES_LOCATIONS[2]
		list = PuzzlePiece.objects.filter(needs_help=True)
		result = [x.puzzle for x in list]
		render = render_to_string(template, {'list':result}, context_instance=RequestContext(request))
		
	elif (newPage == PAGES_FULL[3]):
		template = PAGES_LOCATIONS[3]
		template = PAGES_LOCATIONS[3]
		dajax = Dajax()
		list = Photo.objects.filter(user=request.user)
		pictureGrid = PictureGrid(list).getGridAsString();
		render = render_to_string(template, {'form': get_profile_form(request), 'pictureGrid': pictureGrid}, context_instance=RequestContext(request))
		
	elif (newPage == PAGES_FULL[4]):
		logout(request)
		dajax.redirect("/accounts/login",delay=0) 
		return dajax.json()
	
	dajax.assign('#page-container', 'innerHTML', render)
	return dajax.json()

@dajaxice_register
def find_locations(request, location):
	list = UserProfile.objects.filter(location__icontains = location)
	result = [ResultUser(x).__dict__ for x in list]
	return simplejson.dumps(result)



