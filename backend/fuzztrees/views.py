from django.contrib.auth import authenticate as backend_auth
from django.contrib.auth import login as backend_login
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from openid2rp.django.auth import linkOpenID, preAuthenticate, AX
import os, urllib, random, string
from fuzztrees.models import Graph

from fuzztrees.models import User
from nodes_config import NODE_TYPES

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def teaser(request):
    return render_to_response('teaser.html', {}, context_instance=RequestContext(request))

def editor(request, graph_id):
	graphs=request.user.graphs.all()
	return render_to_response('editor.html', {'graphs' : graphs, 'graph_id' : graph_id, 'node_types' : NODE_TYPES}, context_instance=RequestContext(request))

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
				randomstring=''.join([random.choice(string.letters + string.digits) for i in range(8)])
				newuser=User(username=randomstring)
			newuser.is_active=True
			newuser.save()
			linkOpenID(newuser, user.openid_claim)
			return HttpResponseRedirect('/login/?openid_identifier=%s'%urllib.quote_plus(request.session['openid_identifier']))	
	backend_login(request, user)
	allgraphs=user.graphs.all()
	if len(allgraphs)==0:
		g=Graph(owner=user, type=1)
		g.save()
		return HttpResponseRedirect('/editor/%u'%g.pk)
	else:
		return HttpResponseRedirect('/editor/%u'%allgraphs[0].pk)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')
	
