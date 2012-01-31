'''
Created on Jan 29, 2012

@author:  Wissam Jarjoui (wjarjoui@mit.edu)
'''
from puzzlaef.forms import UserProfileForm
from puzzlaef.main.models import UserProfile
from puzzlaef.main.utils import ResultUser
from puzzlaef.main.pictureGrid import PictureGrid
from puzzlaef.main.pictureThumb import PictureThumb
from puzzlaef.views import PAGES_FULL, PAGES_LOCATIONS, get_profile_form
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.core import serializers
from django.template.loader import render_to_string
from django.utils import simplejson
import string

def assert_access(user):
	if user.is_authenticated():
		return None
	else:
		dajax = Dajax()
	 	dajax.redirect("/accounts/login",delay=0) 
		return dajax.json()


def make_new_puzzle():
	#TODO: Wissam
	return "walka"
	
def getThemes():
	#TODO: Wissam
	return []


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
	elif (newPage == PAGES_FULL[1]):
		template = PAGES_LOCATIONS[1]
	elif (newPage == PAGES_FULL[2]):
		template = PAGES_LOCATIONS[2]
	elif (newPage == PAGES_FULL[3]):
		template = PAGES_LOCATIONS[3]
		render = render_to_string(template, {'form': get_profile_form(request)})
		dajax = Dajax()
		dajax.assign('#page-container', 'innerHTML', render)
		return dajax.json()
	elif (newPage == PAGES_FULL[4]):
		logout(request)
		dajax.redirect("/accounts/login",delay=0) 
		return dajax.json()
	render = render_to_string(template, {})
	dajax.assign('#page-container', 'innerHTML', render)
	return dajax.json()

fakePictureURL = "http://www.blogcdn.com/www.engadget.com/media/2012/01/2012-01-29-sony200_216x150.jpg"
fakePictureTitle = "Great Sunset"
fakePictureSet = [PictureThumb(fakePictureURL,fakePictureURL,fakePictureTitle) for i in range(15)]

@dajaxice_register
def start_puzzle(request, startWith):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess
	
	puzzle_id = make_new_puzzle()
	
	pictureGrid = PictureGrid(fakePictureSet).getGridAsString();
	
	render = render_to_string("puzzle/pickTheme.html", {"startWith":startWith, 'themes': getThemes(), 'pictureGrid': pictureGrid})
	dajax = Dajax()
	dajax.assign('#page-container', 'innerHTML', render)
	dajax.script("initialize_pick_theme('"+ puzzle_id +"')")
	return dajax.json()  


@dajaxice_register
def theme_picked(request, theme):
	assertAccess = assert_access(request.user)
	if(assertAccess):
		return assertAccess

	#render = render_to_string("puzzle/pickTheme.html", {"startWith":startWith, 'themes': getThemes(), 'pictureGrid': pictureGrid})
	dajax = Dajax()
	#dajax.assign('#page-container', 'innerHTML', render)
	#dajax.script("initialize_pick_theme('"+ puzzle_id +"')")
	return dajax.json()

@dajaxice_register
def find_locations(request, location):
	list = UserProfile.objects.filter(location__icontains = location)
	result = [ResultUser(x).__dict__ for x in list]
	return simplejson.dumps(result)



