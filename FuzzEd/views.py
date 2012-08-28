import urllib, datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import mail_managers

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from openid2rp.django.auth import linkOpenID, preAuthenticate, AX, getOpenIDs

from FuzzEd.models import Graph, notations, commands

@require_GET
def index(request):
    if 'logout' in request.GET:
        auth.logout(request)

    if request.user.is_authenticated():
        return redirect('dashboard')

    return render(request, 'index.html', {'pwlogin': ('pwlogin' in request.GET)})

@require_GET
def about(request):
    return render(request, 'util/about.html')

@login_required
@require_http_methods(['GET', 'POST'])
def settings(request):
    POST = request.POST

    if POST.get('save'):
        user    = request.user
        profile = user.get_profile()

        try:
            user.first_name    = POST['first_name']
            user.last_name     = POST['last_name']
            user.email         = POST['email']
            profile.newsletter = bool(POST.get('newsletter'))

            profile.save()
            user.save()

            return redirect('dashboard')

        except KeyError:
            return HttpResponseBadRequest()

    return render(request, 'util/settings.html')

@login_required
@require_GET
def dashboard(request):
    graphs = request.user.graphs.all().filter(deleted=False).order_by('-created')
    parameters = {'graphs': [(notations.by_kind[graph.kind]['name'], graph) for graph in graphs]}

    return render(request, 'dashboard/dashboard.html', parameters)

@login_required
@require_POST
def dashboard_new(request):
    POST = request.POST

    # save the graph
    if POST.get('save') and POST.get('kind') and POST.get('title'):
        commands.AddGraph.create_of(kind=POST['kind'], name=POST['title'], owner=request.user).do()
        return redirect('dashboard')

    # render the create diagram if fuzztree
    elif POST.get('kind') in notations.by_kind:
        kind = POST['kind']
        parameters = {
            'kind': kind,
            'name': notations.by_kind[kind]['name']
        }
        return render(request, 'dashboard/dashboard_new.html', parameters)

    # something is not right with the request
    return HttpResponseBadRequest()

@login_required
@require_http_methods(['GET', 'POST', 'DELETE'])
def dashboard_edit(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
    POST  = request.POST

    # the owner made changes to the graph's field, better save it (if we can)
    if POST.get('save'):
        graph.name = POST.get('name', '')
        graph.save()
        return redirect('dashboard')

    # deletion requested? do it and go back to dashboard
    if POST.get('delete') or request.method == 'DELETE':
        commands.DeleteGraph.of(graph_id).do()
        return redirect('dashboard')

    # please show the edit page to the user on get requests
    if POST.get('edit') or request.method == 'GET':
        parameters = {
            'graph': graph,
            'kind':  notations.by_kind[graph.kind]['name']
        }
        return render(request, 'dashboard/dashboard_edit.html', parameters)

    # something was not quite right here
    raise HttpResponseBadRequest()

@login_required
# TODO: not yet working
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

@require_http_methods(['GET', 'POST'])
def login(request):
    GET  = request.GET
    POST = request.POST

    # user data was transmitted, try login the user one
    if 'loginname' in POST and 'loginpw' in POST:
        user = auth.authenticate(username=POST['loginname'], password=POST['loginpw'])
        # user found? sign-on
        if user is not None and user.is_active:
            auth.login(request, user)

    elif 'openid_identifier' in GET:
        # first stage of OpenID authentication
        open_id = GET['openid_identifier']
        request.session['openid_identifier'] = open_id

        return preAuthenticate(open_id, 'http://%s/login/?openidreturn' % request.get_host())

    elif 'openidreturn' in GET:
        user = auth.authenticate(openidrequest=request)

        if user.is_anonymous():    
            user_name = None
            email     = None

            user_sreg = user.openid_sreg
            user_ax   = user.openid_ax

            # not known to the backend so far, create it transparently
            if 'nickname' in user_sreg:
                user_name = unicode(user_sreg['nickname'],'utf-8')[:29]

            if 'email' in user_sreg:         
                email = unicode(user_sreg['email'],'utf-8')[:29]

            if AX.email in user_ax:
                email = unicode(user_ax[AX.email],'utf-8')[:29]

            # no username given, register user with his e-mail address as username
            if not user_name and email:
                new_user = User(username=email, email=email)

            # both, username and e-mail were not given, use a timestamp as username
            elif not username and not email:
                now = datetime.datetime.now()
                user_name = 'Anonymous %u%u%u%u' % (now.hour, now.minute,\
                                                    now.second, now.microsecond)
                new_user = User(username=user_name)

            # username and e-mail were given; great - register as is
            elif user_name and email:
                new_user = User(username=user_name, email=email)

            # username given but no e-mail - at least we know how to call him
            elif user_name and not email:
                new_user = User(username=user_name)

            if AX.first in user_ax:
                new_user.first_name = unicode(user_ax[AX.first],'utf-8')[:29]

            if AX.last in user_ax:
                new_user.last_name=unicode(user_ax[AX.last],'utf-8')[:29]

            new_user.is_active = True
            new_user.save()

            linkOpenID(new_user, user.openid_claim)
            mail_managers('New user', str(new_user), fail_silently=True)

            return redirect('/login/?openid_identifier=%s' % 
                            urllib.quote_plus(request.session['openid_identifier'])) 

    auth.login(request, user)
    return redirect('dashboard')