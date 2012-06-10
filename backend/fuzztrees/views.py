from django.contrib.auth import authenticate as backend_auth
from django.contrib.auth import login as backend_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from openid2rp.django.auth import linkOpenID, preAuthenticate, AX
import os, urllib, random, string, datetime
from fuzztrees.models import Graph, GraphTypes, History, Commands

from fuzztrees.models import User
from nodes_config import NODE_TYPES

def index(request):
	if "logout" in request.GET:
		auth.logout(request)
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

def about(request):
	return render_to_response('about.html', {}, context_instance=RequestContext(request))

@login_required
def dashboard(request):
	if "new" in request.POST:
		if request.POST['new']=='faulttree':
			g=Graph(owner=request.user)
			g.type=GraphTypes.FAULT_TREE
			g.name="New Fault Tree"
			g.save()
			c=History(command=Commands.ADD_GRAPH, graph=g)
			c.save()
		elif request.POST['new']=='fuzztree':
			g=Graph(owner=request.user)
			g.type=GraphTypes.FUZZ_TREE
			g.name="New FuzzTree"
			g.save()
			c=History(command=Commands.ADD_GRAPH, graph=g)
			c.save()
		elif request.POST['new']=='rbd':
			g=Graph(owner=request.user)
			g.type=GraphTypes.RBD
			g.name="New Reliability Block Diagram"
			g.save()
			c=History(command=Commands.ADD_GRAPH, graph=g)
			c.save()
		else:
			return HttpResponseBadRequest()
	elif "delete" in request.POST and "graph" in request.POST:
		g=get_object_or_404(Graph, pk=request.POST["graph"], owner=request.user)
		g.delete()
	elif "change" in request.POST and "newtitle" in request.POST and "graph" in request.POST:
		g=get_object_or_404(Graph, pk=request.POST["graph"], owner=request.user)
		g.name=request.POST["newtitle"]
		g.save()		
	graphs=request.user.graphs.all()
	return render_to_response('dashboard.html', {'graphs': graphs}, context_instance=RequestContext(request))

@login_required
def dashboard_popup(request, graph_id):
	g=get_object_or_404(Graph, pk=graph_id, owner=request.user)
	return render_to_response('dashboard_popup.html', {'graph': g}, context_instance=RequestContext(request))	

def teaser(request):
    return render_to_response('teaser.html', {}, context_instance=RequestContext(request))

@login_required
def editor(request, graph_id):
	g=get_object_or_404(Graph, pk=graph_id, owner=request.user)
	return render_to_response('editor.html', {'graph' : g, 'node_types' : NODE_TYPES}, context_instance=RequestContext(request))

def login(request):
	#if request.POST:
	#	if 'loginname' in request.POST and 'loginpw' in request.POST:
	#		user=auth.authenticate(username=request.POST['loginname'], password=request.POST['loginpw'])
	#		if user is not None:
	#			if user.is_active:
	#				auth.login(request, user)
	if "openid_identifier" in request.GET:
		# first stage of OpenID authentication
		request.session['openid_identifier']=request.GET['openid_identifier']
		return preAuthenticate(request.GET['openid_identifier'], "http://"+request.get_host()+"/login/?openidreturn")
	elif "openidreturn" in request.GET:
		user = backend_auth(openidrequest=request)
		if user.is_anonymous():		
			# not know to the backend so far, create it transparently
			if 'nickname' in user.openid_sreg:
				newuser=User(username=unicode(user.openid_sreg['nickname'],'utf-8'))
			elif 'email' in user.openid_sreg:
				newuser=User(username=unicode(user.openid_sreg['email'],'utf-8'))
			elif AX.email in user.openid_ax:
				newuser=User(username=unicode(user.openid_ax[AX.email],'utf-8'))
			else:
				d=datetime.datetime.now()
				randomname="Anonymous%u%u%u%u"%(d.hour,d.minute,d.second,d.microsecond)
				newuser=User(username=randomname)
			newuser.is_active=True
			newuser.save()
			linkOpenID(newuser, user.openid_claim)
			return HttpResponseRedirect('/login/?openid_identifier=%s'%urllib.quote_plus(request.session['openid_identifier']))	
	backend_login(request, user)
	#allgraphs=user.graphs.all()
	#if len(allgraphs)==0:
	#	g=Graph(owner=user, type=1)
	#	g.save()
	#	return HttpResponseRedirect('/editor/%u'%g.pk)
	#else:
	#	return HttpResponseRedirect('/editor/%u'%allgraphs[0].pk)
	return HttpResponseRedirect('/dashboard/')
	
