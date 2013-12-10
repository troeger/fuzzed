import settings

def footer(request):
    return {'version': settings.VERSION}  # if this fails, run fab build.configs
