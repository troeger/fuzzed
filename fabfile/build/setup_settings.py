settings='''
# Autogenerated by 'fab build.configs'.
# Do not edit.

import os.path, logging

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

%(conf_lines)s

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.%(db_type)s', 
        'NAME':     '%(db_name)s',  
        'TEST_NAME':'%(db_test_name)s',                      
        'USER':     '%(db_user)s',                              
        'PASSWORD': '%(db_password)s',                       
        'HOST':     '%(db_host)s',                                       
        'PORT':     '',                                       
    }
}

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    %(add_static_finders)s
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    %(add_context_processors)s
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    %(add_middleware)s
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    %(add_installed_apps)s
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level':   'DEBUG',
            'class':   'logging.StreamHandler'
        },
        'mail_admins': {
            'level':   'ERROR',
            'class':   'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },        
        'False': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':  ['%(logger_requests)s'],
            'level':     'ERROR',
            'propagate': True,
        },
        'FuzzEd': {
            'handlers':  ['%(logger_fuzzed)s'],
            'level':     'DEBUG',
            'propagate': True,
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    %(add_auth_backends)s
)
'''

import ConfigParser, os

def configOptions(confFile, sectionPrefixes):
    ''' Parse settings.ini and deliver content.
        The argument defines a list of section prefixes for sections
        that should be considered.
    '''
    sections = []
    conf = ConfigParser.ConfigParser()
    conf.optionxform = str   # preserve case in keys
    conf.read(confFile)
    for sec in conf.sections():
        for prefix in sectionPrefixes:
            if sec.startswith(prefix):
                sections.append(sec)
    for section in sections:
        for key, value in conf.items(section):
            yield (section, key, value)

def createBackendSettings(confFile, forDevelopment):
    ''' Parse settings.ini and create a dedicated daemon.ini
        for the backend daemon. It needs the DB credentials for notification channels,
        and the list of backend service settings.
    '''
    conf_lines = ["# Autogenerated by 'fab build.configs'.\n# Do not edit.\n","[db]"]    
    current_section = ""
    if forDevelopment:
        prefixes = ['all', 'development', 'backend_']
    else:
        prefixes = ['all', 'production', 'backend_']        
    for section, key, value in configOptions(confFile, prefixes):
        if key.startswith('db_'):
            conf_lines.append("%s = %s"%(key, value))
        elif section.startswith('backend_'):
            if section != current_section:
                conf_lines.append('\n[%s]'%section)
                current_section = section
            conf_lines.append("%s = %s"%(key, value))
    return '\n'.join(conf_lines)

def createDjangoSettings(confFile, forDevelopment):
    ''' Parse settings.ini and fill the upper template.
        The result is a valid Django setttings.py file,
        based on the configuration from the INI file.
        The argument tells the special section in the
        INI file that is considered beside 'all'.
    '''
    replacements = {}
    conf_lines = []
    # Read ip address from Vagrant-generated file
    ip = None
    if socket.getfqdn() == 'precise64':
        ip = "192.168.33.10"
        print 'Using Vagrant IP: ' + ip
    if forDevelopment:
        prefixes = ['all', 'development']
    else:
        prefixes = ['all', 'production']          
    for section, key, value in configOptions(confFile, prefixes):
        if key.isupper():
            if key == 'OPENID_RETURN' and ip:
                value = "'http://%s:8000/login/?openidreturn'" % ip
            if key == 'SERVER' and ip:
                value = "'http://%s:8000'" % ip
            # Add the configuration from the INI file directly
            conf_lines.append('%s=%s'%(key, value))
        else:
            # Register it as replacement value
            replacements[key] = value
    replacements['conf_lines']='\n'.join(sorted(conf_lines))
    return settings%replacements

