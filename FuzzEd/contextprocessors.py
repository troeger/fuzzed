import FuzzEd

def footer(request):
    return {'fuzzed_version': FuzzEd.__version__}
