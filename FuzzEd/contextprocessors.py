import settings

def footer(request):
    return {'version': settings.VERSION}
