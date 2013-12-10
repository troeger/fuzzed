from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotModified, \
    HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseGone, \
    HttpResponseServerError

class FuzzEdException(Exception):
    ''' 
    As of Python 2.7, BaseException has no more default message attribute.
    We therefore define our own base class for this.
    '''
    _message=""
    def _get_message(self): 
        return self._message
    def _set_message(self, message): 
        self._message = message
    def __init__(self, message=''):
        self.message = message
    message = property(_get_message, _set_message)

class HttpResponseRedirectAnswer(Exception):
    def __init__(self, target):
        self.target = target
    def result(self):
        return HttpResponseRedirect(self.target)

class HttpResponsePermanentRedirectAnswer(Exception):
    def __init__(self, target):
        self.target = target
    def result(self):
        return HttpResponsePermanentRedirect(self.target)

class HttpResponseNotModifiedAnswer(FuzzEdException):
    def result(self):
        return HttpResponseNotModified(self.message)

class HttpResponseBadRequestAnswer(FuzzEdException):
    def result(self):
        return HttpResponseBadRequest(self.message)

class HttpResponseNotFoundAnswer(FuzzEdException):
    def result(self):
        return HttpResponseNotFound(self.message)

class HttpResponseForbiddenAnswer(FuzzEdException):
    def result(self):
        return HttpResponseForbidden(self.message)

class HttpResponseNotAllowedAnswer(Exception):
    def __init__(self, allowedMethods):
        self.allowedMethods = allowedMethods
    def result(self):
        return HttpResponseNotAllowed(self.allowedMethods)

class HttpResponseGoneAnswer(FuzzEdException):
    def result(self):
        return HttpResponseGone(self.message)

class HttpResponseServerErrorAnswer(FuzzEdException):
    def result(self):
        return HttpResponseServerError(self.message)

class HttpResponseCreated(HttpResponse):
    status_code = 201

class HttpResponseCreatedAnswer(Exception):
    def result(self):
        return HttpResponseCreated() 

class HttpResponseNoResponse(HttpResponse):
    status_code = 204

class HttpResponseAccepted(HttpResponse):
    status_code = 202

class HttpResponseNoResponseAnswer(FuzzEdException):
    def result(self):
        return HttpResponseNoResponse(self.message)

class HttpErrorMiddleware(object):
    def process_exception(self, request, exception):
        if hasattr(exception, 'result'):
            return exception.result()
        else:
            # default exception handling kicks in
            return None