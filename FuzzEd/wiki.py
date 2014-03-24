try:
	from wikimarkup import parse, registerInternalLinkHook
except Exception as e:
	print "Please install py-wikimarkup first (https://github.com/dcramer/py-wikimarkup/)"
	raise e

# Our markup renderer implementation, simply relaying to wikimarkup
def render(src):
	return parse(src)

class FuzzEdWikiAccess(object):
	''' The authorization setup for the documentation pages. '''
	def can_view(self, request, target):
		''' Let Google index our stuff. '''
		return True

	def can_create(self, request, target):
		''' 
			Only edit links are visible for the ordinary users. 
			Page creation works magically for admins with /docs/<name>/edit,
			which should be improved in the future.
		'''
		return request.user.is_authenticated() and request.user.is_superuser

	def can_edit(self, request, target):
		''' Keep spammers away. '''
		return request.user.is_authenticated() 

	def can_view_history(self, request, target):
		''' Views are currently broken. '''
		return False

''' Support internal Wiki links.'''
def internalLinkHook(parser_env, namespace, body):
	return '<a href="heise.de">Heise</a>'

registerInternalLinkHook(None, internalLinkHook)
