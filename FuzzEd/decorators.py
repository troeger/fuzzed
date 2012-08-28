from django.http import HttpResponseBadRequest

def require_ajax(request_handler):
    """
    Function: require_ajax
    
    This function is a view decorator that restricts the incoming request to be an AJAX one
    
    Arguments:
     {function} request_handler - the handler that is executed if the request is AJAX
    
    Returns:
     {function} wrapped request_handler
    """  
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return request_handler(request, *args, **kwargs)
    wrap.__doc__  = request_handler.__doc__
    wrap.__name__ = request_handler.__name__
    
    return wrap