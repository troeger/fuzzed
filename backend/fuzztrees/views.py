from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

def teaser(request):
    return render_to_response('teaser.html', {}, context_instance=RequestContext(request))

def login(request):
	if request.POST:
		if "loginname" in request.POST and "loginpw" in request.POST:
			user=authenticate(request.POST["loginname"], request.POST["loginpw"])
			if user is not None:
				if user.is_active:
					login(request, user)
	return HttpResponseRedirect("/")

def logout(request):
	logout(request)
	return HttpResponseRedirect("/")
	