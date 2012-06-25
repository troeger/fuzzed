from django.contrib.auth import authenticate as backend_auth
from django.contrib.auth import login as backend_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.mail import mail_managers
from fuzztrees.middleware import HttpResponseBadRequest
from openid2rp.django.auth import linkOpenID, preAuthenticate, AX, getOpenIDs
import os, urllib, random, string, datetime
from fuzztrees.models import Graph, GraphTypes, History, Commands, createFuzzTreeGraph, delGraph, renameGraph

from fuzztrees.models import User
from nodes_config import NODE_TYPES

def index(request):
	if "logout" in request.GET:
		auth.logout(request)
	return render_to_response('index.html', {'pwlogin': ('pwlogin' in request.GET)}, context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html', {}, context_instance=RequestContext(request))

@login_required
def settings(request):
	return render_to_response('settings.html', {'user': request.user, 'openids': getOpenIDs(request.user)}, context_instance=RequestContext(request))

@login_required
def dashboard(request):
	if "new" in request.POST and "type" in request.POST and "title" in request.POST:
		if request.POST['type']=='faulttree':
			raise HttpResponseBadRequest()
		elif request.POST['type']=='fuzztree':
			createFuzzTreeGraph(request.user, request.POST['title'])
		elif request.POST['type']=='rbd':
			raise HttpResponseBadRequest()
		else:
			raise HttpResponseBadRequest()
	elif "delete" in request.POST and "graph" in request.POST:
		g=get_object_or_404(Graph, pk=request.POST["graph"], owner=request.user)
		delGraph(g)
	elif "change" in request.POST and "newtitle" in request.POST and "graph" in request.POST:
		g=get_object_or_404(Graph, pk=request.POST["graph"], owner=request.user)
		renameGraph(g, request.POST["newtitle"])
	elif "settings_save" in request.POST:
		if "email" in request.POST:
			request.user.email=request.POST["email"];
		if "firstname" in request.POST:
			request.user.first_name=request.POST["firstname"];			
		if "lastname" in request.POST:
			request.user.last_name=request.POST["lastname"];			
		if "newsletter" in request.POST:
			if request.POST["newsletter"] == "on":
				prof=request.user.get_profile()
				prof.newsletter=True
				prof.save()
		else:
			prof=request.user.get_profile()
			prof.newsletter=False
			prof.save()
		request.user.save()		
	graphs=request.user.graphs.all().filter(deleted=False)
	return render_to_response('dashboard.html', {'graphs': graphs}, context_instance=RequestContext(request))

@login_required
def dash_new(request):
	return render_to_response('dash_new.html', {'type':request.POST['type']}, context_instance=RequestContext(request))	

@login_required
def dash_change(request, graph_id):
	g=get_object_or_404(Graph, pk=graph_id, owner=request.user)
	return render_to_response('dash_change.html', {'graph': g}, context_instance=RequestContext(request))	

def teaser(request):
    return render_to_response('teaser.html', {}, context_instance=RequestContext(request))

@login_required
def editor(request, graph_id):
	g=get_object_or_404(Graph, pk=graph_id, owner=request.user)
	return render_to_response('editor.html', {'graph' : g, 'node_types' : NODE_TYPES}, context_instance=RequestContext(request))

def login(request):
	if request.POST:
		if 'loginname' in request.POST and 'loginpw' in request.POST:
			user=auth.authenticate(username=request.POST['loginname'], password=request.POST['loginpw'])
			if user is not None:
				if user.is_active:
					auth.login(request, user)
	elif "openid_identifier" in request.GET:
		# first stage of OpenID authentication
		request.session['openid_identifier']=request.GET['openid_identifier']
		return preAuthenticate(request.GET['openid_identifier'], "http://"+request.get_host()+"/login/?openidreturn")
	elif "openidreturn" in request.GET:
		user = backend_auth(openidrequest=request)
		if user.is_anonymous():		
			username=None
			# not known to the backend so far, create it transparently
			if 'nickname' in user.openid_sreg:
				username=unicode(user.openid_sreg['nickname'],'utf-8')[:29]
			if 'email' in user.openid_sreg:			
				email=unicode(user.openid_sreg['email'],'utf-8')[:29]
			if AX.email in user.openid_ax:
				email=unicode(user.openid_ax[AX.email],'utf-8')[:29]
			if not username and email:
				newuser=User(username=email, email=email)
			elif not username and not email:
				d=datetime.datetime.now()
				username="Anonymous%u%u%u%u"%(d.hour,d.minute,d.second,d.microsecond)
				newuser=User(username=username)
			elif username and email:
				newuser=User(username=username, email=email)
			elif username and not email:
				newuser=User(username=username)
			if AX.first in user.openid_ax:
				newuser.first_name=unicode(user.openid_ax[AX.first],'utf-8')[:29]
			if AX.last in user.openid_ax:
				newuser.last_name=unicode(user.openid_ax[AX.last],'utf-8')[:29]
			newuser.is_active=True
			newuser.save()
			linkOpenID(newuser, user.openid_claim)
			mail_managers("New user", str(newuser), fail_silently=True)
			return HttpResponseRedirect('/login/?openid_identifier=%s'%urllib.quote_plus(request.session['openid_identifier']))	
	backend_login(request, user)
	return HttpResponseRedirect('/dashboard/')
	
