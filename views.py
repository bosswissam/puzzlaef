from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from puzzlaef.forms import UserProfileForm

PAGES = ['Play', 'Discover', 'Help a Puzzlaef']
PAGES_FULL = PAGES + ['Settings', 'Logout']
PAGES_LOCATIONS = ['pageTemplates/play.html', 'pageTemplates/discover.html', 'pageTemplates/helpPuzzlaef.html', 'pageTemplates/profile.html', 'registration/logout.html']

def start(request):
	if request.user.is_authenticated():
	    # TODO: show profile
		form = UserProfileForm(data=request.POST)
		return render_to_response('pageTemplates/page_layout.html', RequestContext(request, {'pages': PAGES, 'current_page': PAGES_FULL[0], 'current_page_template': PAGES_LOCATIONS[0] }))
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

