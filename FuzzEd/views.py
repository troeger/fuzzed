import urllib, datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import mail_managers

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from openid2rp.django.auth import linkOpenID, preAuthenticate, AX, getOpenIDs

from FuzzEd.models import Graph, notations, commands

def index(request):
    if 'logout' in request.GET:
        auth.logout(request)

    if request.user.is_authenticated():
        return redirect('dashboard')

    return render(request, 'index.html', {'pwlogin': ('pwlogin' in request.GET)})

def about(request):
    return render(request, 'util/about.html')

@login_required
def settings(request):
    parameters = {
        'user':    request.user,
        'openids': getOpenIDs(request.user)
    }

    return render(request, 'settings.html', parameters)

@login_required
def dashboard(request):
    post = request.POST

    if 'settings_save' in post:
        if 'email' in post:
            request.user.email = post['email']

        if 'firstname' in post:
            request.user.first_name = post['firstname']

        if 'lastname' in post:
            request.user.last_name = post['lastname']

        if 'newsletter' in post and post['newsletter'] == 'on':
            profile = request.user.get_profile()
            profile.newsletter = True
            profile.save()
        else:
            profile = request.user.get_profile()
            profile.newsletter = False
            profile.save()
        request.user.save()

    graphs = request.user.graphs.all().filter(deleted=False).order_by('-created')
    parameters = {'graphs': [(notations.by_kind[graph.kind]['name'], graph) for graph in graphs]}

    return render(request, 'dashboard/dashboard.html', parameters)

@login_required
def dashboard_new(request):
    post = request.POST

    # save the graph
    if post.get('save') and post.get('kind') and post.get('title'):
        commands.AddGraph.create_of(kind=post['kind'], name=post['title'], owner=request.user).do()
        return redirect('dashboard')

    # render the create diagram if fuzztree
    elif post.get('kind') in notations.by_kind:
        kind = post['kind']
        parameters = {
            'kind': kind,
            'name': notations.by_kind[kind]['name']
        }
        return render(request, 'dashboard/dashboard_new.html', parameters)

    # something is not right with the request
    return HttpResponseBadRequest()

@login_required
def dashboard_edit(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
    post = request.POST

    # the owner made changes to the graph's field, better save it (if we can)
    if post.get('save'):
        try:
            commands.ChangeGraph.of(graph_id, name=post.get('title')).do()
            return redirect('dashboard')

        except ObjectDoesNotExist, MultipleObjectsReturned:
            return HttpResponseBadRequest()

    # user decided to cancel the changes to the graph, go back to main page
    if post.get('cancel'):
        return redirect('dashboard')

    # deletion requested? do it and go back to dashboard
    if post.get('delete') or request.method == 'DELETE':
        try:
            commands.DeleteGraph.of(graph_id).do()
            return redirect('dashboard')

        except ObjectDoesNotExist, MultipleObjectsReturned:
            return HttpResponseBadRequest()

    # please show the edit page to the user on get requests
    if post.get('edit') or request.method == 'GET':
        parameters = {
            'graph': graph,
            'kind':  notations.by_kind[graph.kind]['name']
        }
        return render(request, 'dashboard/dashboard_edit.html', parameters)

    # something was not quite right here
    return HttpResponseBadRequest()

@login_required
def editor(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
    notation = notations.by_kind[graph.kind]
    nodes = notation['nodes']

    parameters = {
        'graph': graph,
        'graph_notation': notation,
        'nodes': {node: nodes[node] for node in notation['shapeMenuNodeDisplayOrder']}
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
        user = auth.authenticate(openidrequest=request)
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

    auth.login(request, user)

    return redirect('dashboard')