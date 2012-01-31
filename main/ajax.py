'''
Created on Jan 29, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from puzzlaef.forms import UserProfileForm
from puzzlaef.main.models import UserProfile
from puzzlaef.main.utils import ResultUser
from puzzlaef.main.pictureGrid import PictureGrid
from puzzlaef.main.pictureThumb import PictureThumb
from puzzlaef.puzzle.models import Puzzle
from puzzlaef.views import PAGES_FULL, PAGES_LOCATIONS, get_profile_form
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

import string

def assert_access(user):
	if user.is_authenticated():
		return None
	else:
		dajax = Dajax()
	 	dajax.redirect("/accounts/login",delay=0) 
		return dajax.json()
		

def fetch_user_puzzles(request):
	list1 = set(Puzzle.objects.filter(player1=request.user))
	list2 = set(Puzzle.objects.filter(player2=request.user))
	return list(list1.union(list2))

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
def changePage(request, newPage):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess
	
	dajax = Dajax()
	if (newPage == PAGES_FULL[0]):
		template = PAGES_LOCATIONS[0]
		print fetch_user_puzzles(request)
		render = render_to_string(template, {'puzzles': fetch_user_puzzles(request), 'empty': []})
		
	elif (newPage == PAGES_FULL[1]):
		template = PAGES_LOCATIONS[1]
		render = render_to_string(template, {})
		
	elif (newPage == PAGES_FULL[2]):
		template = PAGES_LOCATIONS[2]
		render = render_to_string(template, {})
		
	elif (newPage == PAGES_FULL[3]):
		template = PAGES_LOCATIONS[3]
		render = render_to_string(template, {'form': get_profile_form(request)}, context_instance=RequestContext(request))
		
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



