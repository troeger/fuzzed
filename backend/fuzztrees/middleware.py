from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotModified,	HttpResponseBadRequest,	HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseGone, HttpResponseServerError

class HttpResponseRedirectAnswer(Exception):
	def __init__(self, target):
		self.target=target
	def result(self):
		return HttpResponseRedirect(target)

class HttpResponsePermanentRedirectAnswer(Exception):
	def __init__(self, target):
		self.target=target
	def result(self):
		return HttpResponsePermanentRedirect(target)

class HttpResponseNotModifiedAnswer(Exception):
	def result(self):
		return HttpResponseNotModified()

class HttpResponseBadRequestAnswer(Exception):
	def result(self):
		return HttpResponseBadRequest()

class HttpResponseNotFoundAnswer(Exception):
	def result(self):
		return HttpResponseNotFound()

class HttpResponseForbiddenAnswer(Exception):
	def result(self):
		return HttpResponseForbidden()

class HttpResponseNotAllowedAnswer(Exception):
	def __init__(self, allowedMethods):
		self.allowedMethods=allowedMethods
	def result(self):
		return HttpResponseNotAllowed(allowedMethods) 

class HttpResponseGoneAnswer(Exception):
	def result(self):
		return HttpResponseGone()

class HttpResponseServerAnswer(Exception):
	def result(self):
		return HttpResponseServerError()

class HttpResponseCreated(HttpResponse):
	status_code=201

class HttpResponseCreatedAnswer(Exception):
	def result(self):
		return HttpResponseCreated() 

class HttpResponseNoResponse(HttpResponse):
	status_code=204

class HttpResponseNoResponseAnswer(Exception):
	def result(self):
		return HttpResponseNoResponse()


class HttpErrorMiddleware(object):
	def process_exception(self, request, exception):
		if hasattr(exception, "result"):
			return exception.result()
		else:
			return None 	# default exception handling kicks in
