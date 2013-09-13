import urllib, datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import mail_managers

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from openid2rp.django.auth import linkOpenID, preAuthenticate, AX, IncorrectClaimError
from FuzzEd.models import Graph, notations, commands
import FuzzEd.settings

GREETINGS = [
    'Loading the FuzzEd User Experience',
    'Trying to find your Data... it was here somewhere',
    'Fiddeling with your Graph... Stand by!',
    'Loading good Karma into your Browser',
    'Calculating the Answer to Life...',
    'Man, this takes like for ever to load...',
    'Time to grab some Coffee!'
]

def index(request):
    """
    Function: index
    
    This is the view handler for loading the landing page of the editor. The index.html is rendered unless the user is
    already signed in and being redirected to his or her dashboard.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    if 'logout' in request.GET:
        auth.logout(request)

    if request.user.is_authenticated():
        return redirect('dashboard')

    return render(request, 'index.html', {'pwlogin': ('pwlogin' in request.GET)})

def about(request):
    """
    Function: about
    
    Simple rendering of the about page.
    
    Parameters:
     {HttpRequest} request - a django request
    
    Returns:
     {HttpResponse} a django response object
    """
    return render(request, 'util/about.html')

@login_required
def dashboard(request):
    """
    Function: dashboard
    
    This view handler renders the dashboard of the user. It lists all the graphs of the user that are not marked as
    deleted ordered descending by its creation date. Also, a user is able to create new graphs and edit or delete
    existing graphs from here.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    graphs = request.user.graphs.filter(deleted=False).order_by('-created')
    parameters = {'graphs': [(notations.by_kind[graph.kind]['name'], graph) for graph in graphs]}

    return render(request, 'dashboard/dashboard.html', parameters)

@login_required
def dashboard_new(request):
    """
    Function: dashboard_new
    
    This handler is responsible for rendering a dialog to the user to create a new diagram. It is also responsible for
    processing a save request of such a 'new diagram' request and forwards the user to the dashboard after doing so.
    
    Parameters:
     {HttpRequest} request - a django http request object
    
    Returns:
     {HttpResponse} a django response object
    """
    POST = request.POST

    # save the graph
    if POST.get('save') and POST.get('kind') and POST.get('name'):
        commands.AddGraph.create_from(kind=POST['kind'], name=POST['name'], owner=request.user).do()
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
def dashboard_edit(request, graph_id):
    """
    Function: dashboard_edit
    
    This handler function is responsible for allowing the user to edit the properties of an already existing graph.
    Therefore the system renders a edit dialog to the user where changes can be made and saved or the graph can be
    deleted.
    
    Parameters:
     {HttpResponse} request  - a django request object
     {int}          graph_id - the graph to be edited
    
    Returns:
     {HttpResponse} a django response object
    """
    graph = get_object_or_404(Graph, pk=graph_id, owner=request.user)
    POST  = request.POST

    # the owner made changes to the graph's field, better save it (if we can)
    if POST.get('save'):
        graph.name = POST.get('name', '')
        graph.save()
        messages.add_message(request, messages.SUCCESS, 'Graph saved.')
        return redirect('dashboard')

    # deletion requested? do it and go back to dashboard
    elif POST.get('delete'):
        commands.DeleteGraph.create_from(graph_id).do()
        messages.add_message(request, messages.SUCCESS, 'Graph deleted.')
        return redirect('dashboard')

    # copy requested
    elif POST.get('copy'):
        old_graph = Graph.objects.get(pk=graph_id)
        duplicate_command = commands.AddGraph.create_from(kind=old_graph.kind, name=old_graph.name + ' (copy)',
                                                          owner=request.user,  add_default_nodes=False)
        duplicate_command.do()
        new_graph = duplicate_command.graph

        new_graph.copy_values(old_graph)
        new_graph.save()

        messages.add_message(request, messages.SUCCESS, 'Graph duplicated.')
        return redirect('dashboard')

    elif POST.get('snapshot'):
        old_graph = Graph.objects.get(pk=graph_id)
        duplicate_command = commands.AddGraph.create_from(kind=old_graph.kind, name=old_graph.name + ' (snapshot)',
                                                          owner=request.user, add_default_nodes=False)
        duplicate_command.do()
        new_graph = duplicate_command.graph

        new_graph.copy_values(old_graph)
        new_graph.read_only = True
        new_graph.save()

        messages.add_message(request, messages.SUCCESS, 'Created snapshot.')
        return redirect('dashboard')


    # please show the edit page to the user on get requests
    elif POST.get('edit') or request.method == 'GET':
        parameters = {
            'graph': graph,
            'kind':  notations.by_kind[graph.kind]['name']
        }
        return render(request, 'dashboard/dashboard_edit.html', parameters)

    # something was not quite right here
    raise HttpResponseBadRequest()

@login_required
def settings(request):
    """
    Function: settings
    
    This view handler shows user its settings page. However, if the user is doing some changes to its profile and posts
    the changes to this handler, it will change the underlying user object and redirect afterwards to the dashboard.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
    POST = request.POST

    if POST.get('save'):
        user    = request.user
        profile = user.profile

        user.first_name    = POST.get('first_name', user.first_name)
        user.last_name     = POST.get('last_name', user.last_name)
        user.email         = POST.get('email', user.email)
        profile.newsletter = bool(POST.get('newsletter'))

        profile.save()
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Settings saved.')
        return redirect('dashboard')

    return render(request, 'util/settings.html')

@login_required
def editor(request, graph_id):
    """
    Function: editor
    
    View handler for loading the editor. It just tries to locate the graph to be opened in the editor and passes it to
    its according view.
    
    Parameters:
     {HttpRequest} request  - a django request object
     {int}         graph_id - the id of the graph to be opened in the editor
    
    Returns:
     {HttpResponse} a django response object
    """
    if request.user.is_staff:
        graph    = get_object_or_404(Graph, pk=graph_id)
    else:
        graph    = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    if graph.read_only:
        return HttpResponseBadRequest()

    notation = notations.by_kind[graph.kind]
    nodes    = notation['nodes']

    parameters = {
        'graph':          graph,
        'graph_notation': notation,
        'nodes':          [(node, nodes[node]) for node in notation['shapeMenuNodeDisplayOrder']],
        'greetings':      GREETINGS
    }

    return render(request, 'editor/editor.html', parameters)

@login_required
def snapshot(request, graph_id):
    """
    Function: snapshot
    
    View handler for loading the snapshot viewer. It just tries to locate the graph to be opened 
    and passes it to its according view. For the moment, this is the editor itself, were the JavaScript
    code handles the read-only mode from UI perspective.
    
    Parameters:
     {HttpRequest} request  - a django request object
     {int}         graph_id - the id of the graph to be opened in the snapshot viewer
    
    Returns:
     {HttpResponse} a django response object
    """
    if request.user.is_staff:
        graph    = get_object_or_404(Graph, pk=graph_id)
    else:
        graph    = get_object_or_404(Graph, pk=graph_id, owner=request.user, deleted=False)
    if not graph.read_only:
        return HttpResponseBadRequest()

    notation = notations.by_kind[graph.kind]
    nodes    = notation['nodes']

    parameters = {
        'graph':          graph,
        'graph_notation': notation,
        'nodes':          [(node, nodes[node]) for node in notation['shapeMenuNodeDisplayOrder']],
        'greetings':      GREETINGS
    }

    return render(request, 'editor/editor.html', parameters)


@require_http_methods(['GET', 'POST'])
def login(request):
    """
    Function: login
    
    View handler for loging in a user using OpenID. If the user is not yet know to the system a new profile is created
    for him using his or her personal information as provided by the OpenID provider.
    
    Parameters:
     {HttpRequest} request - a django request object
    
    Returns:
     {HttpResponse} a django response object
    """
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

        try:
           return preAuthenticate(open_id, FuzzEd.settings.OPENID_RETURN)
        except IncorrectClaimError:
           messages.add_message(request, messages.ERROR, 'This OpenID claim is not valid.')
           return redirect('index')

    elif 'openidreturn' in GET:
        user = auth.authenticate(openidrequest=request)

        if user.is_anonymous():    
            user_name = None
            email     = None

            user_sreg = user.openid_sreg
            user_ax   = user.openid_ax

            # not known to the backend so far, create it transparently
            if 'nickname' in user_sreg:
                user_name = unicode(user_sreg['nickname'], 'utf-8')[:29]

            if 'email' in user_sreg:         
                email = unicode(user_sreg['email'], 'utf-8')[:29]

            if AX.email in user_ax:
                email = unicode(user_ax[AX.email], 'utf-8')[:29]

            # no username given, register user with his e-mail address as username
            if not user_name and email:
                # Google is using different claim IDs for the same user, if he comes
                # from different originating domains
                # This leads to a problem when user come from "www" or without "www"
                # In this case, the new username already exists in the database
                try:
                    old_user = User.objects.get(username=email)
                    new_user = User(username=email + '2', email=email)
                except:
                    new_user = User(username=email, email=email)

            # both, username and e-mail were not given, use a timestamp as username
            elif not user_name and not email:
                now = datetime.datetime.now()
                user_name = 'Anonymous %d%d%d%d' % (now.hour, now.minute, now.second, now.microsecond)
                new_user = User(username=user_name)

            # username and e-mail were given; great - register as is
            elif user_name and email:
                new_user = User(username=user_name, email=email)

            # username given but no e-mail - at least we know how to call him
            elif user_name and not email:
                new_user = User(username=user_name)

            if AX.first in user_ax:
                new_user.first_name = unicode(user_ax[AX.first], 'utf-8')[:29]

            if AX.last in user_ax:
                new_user.last_name=unicode(user_ax[AX.last], 'utf-8')[:29]

            new_user.is_active = True
            new_user.save()

            linkOpenID(new_user, user.openid_claim)
            mail_managers('New user', str(new_user), fail_silently=True)

            return redirect('/login/?openid_identifier=%s' % 
                            urllib.quote_plus(request.session['openid_identifier'])) 

        auth.login(request, user)
    return redirect('dashboard')
