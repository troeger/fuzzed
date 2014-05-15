from django.http import HttpResponseBadRequest

def require_ajax(function=None,redirect_field_name=None):
    """
    Function: require_ajax
    
    This function is a view decorator that restricts the incoming request to be an AJAX one
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.is_ajax():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseBadRequest()
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)

