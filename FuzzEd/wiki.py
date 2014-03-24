try:
	from wikimarkup import parse
except:
	print "Please install py-wikimarkup first (https://github.com/dcramer/py-wikimarkup/)"

def render(src):
	return parse(src)


