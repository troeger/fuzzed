import os, urllib, random, string, datetime

from django.contrib.auth import authenticate as backend_auth
from django.contrib.auth import login as backend_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.core.mail import mail_managers

from openid2rp.django.auth import linkOpenID, preAuthenticate, AX, getOpenIDs

from FuzzEd.model import Graph, Command, UserProfile, notations
from FuzzEd.middleware import HttpResponseBadRequest

def index(request):
	if 'logout' in request.GET:
		auth.logout(request)

	if request.user.is_authenticated():
		return redirect('dashboard')

	return render_to_response('index.html', {'pwlogin': ('pwlogin' in request.GET)}, context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html', {}, context_instance=RequestContext(request))

@login_required
def settings(request):
	parameters = {
		'user': request.user,
		'openids': getOpenIDs(request.user)
	}

	return render_to_response('settings.html', parameters, context_instance=RequestContext(request))

@login_required
def dashboard(request):
	if 'settings_save' in request.POST:
		if 'email' in request.POST:
			request.user.email = request.POST['email']

		if 'firstname' in request.POST:
			request.user.first_name = request.POST['firstname']

		if 'lastname' in request.POST:
			request.user.last_name = request.POST['lastname']

		if 'newsletter' in request.POST and request.POST['newsletter'] == 'on':
			prof = request.user.get_profile()
			prof.newsletter = True
			prof.save()

		else:
			prof = request.user.get_profile()
			prof.newsletter = False
			prof.save()

		request.user.save()
	graphs = request.user.graphs.all().filter(deleted=False)

	return render_to_response('dashboard/dashboard.html', {'graphs': graphs}, context_instance=RequestContext(request))

@login_required
def dashboard_new(request):
	# save the graph
	if 'save' in request.POST and 'type' in request.POST and 'title' in request.POST:
		if request.POST['type'] == 'fuzztree':
			createFuzzTreeGraph(request.user, request.POST['title'])

		return redirect('dashboard')

	# render the create diagram template
	elif not 'type' in request.POST or 'type' in request.POST and request.POST['type'] == 'fuzztree':
		parameters = {
			'type': 'fuzztree',
			'name': 'FuzzTree'
		}
		return render_to_response('dashboard/dashboard_new.html', parameters, context_instance=RequestContext(request))
	
	# something is not right with the request
	raise HttpResponseBadRequest()

@login_required
def dashboard_edit(request, graph_id):
	graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
	
	if 'delete' in request.POST:
		deleted_graph = str(graph)
		delGraph(graph)
		return render_to_response('dashboard/dashboard.html', {'deleted_graph': deleted_graph})

	if 'save' in request.POST:
		renameGraph(graph, request.POST['title'])
		return redirect('dashboard')	

	return render_to_response('dashboard/dashboard_edit.html', {'graph': graph}, context_instance=RequestContext(request))

@login_required
def editor(request, graph_id):
	graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
	parameters = {
		'graph': graph,
		'nodes_types': notations.by_kind[graph.kind]
	}

	return render_to_response('editor.html', parameters, context_instance=RequestContext(request))

def login(request):
	if request.POST:
		if 'loginname' in request.POST and 'loginpw' in request.POST:
			user=auth.authenticate(username=request.POST['loginname'], password=request.POST['loginpw'])
			if user is not None:
				if user.is_active:
					auth.login(request, user)

	elif 'openid_identifier' in request.GET:
		# first stage of OpenID authentication
		request.session['openid_identifier']=request.GET['openid_identifier']
		return preAuthenticate(request.GET['openid_identifier'], 'http://' + request.get_host() + '/login/?openidreturn')

	elif 'openidreturn' in request.GET:
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
				username='Anonymous%u%u%u%u' % (d.hour,d.minute,d.second,d.microsecond)
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
			mail_managers('New user', str(newuser), fail_silently=True)
			return redirect('/login/?openid_identifier=%s'%urllib.quote_plus(request.session['openid_identifier']))	

	backend_login(request, user)

	return redirect('dashboard')