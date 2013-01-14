import FuzzEd

def footer(request):
	result = {'fuzzed_version': FuzzEd.__version__}
	return result
