ADMINS = (
    ('Peter Troeger', 'peter.troeger@hpi.uni-potsdam.de'),
)
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = '[FuzzEd] '

DEBUG                   = False
TEMPLATE_DEBUG          = DEBUG
SEND_BROKEN_LINK_EMAILS = False     
EMAIL_BACKEND           = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL            = 'webmaster@fuzztrees.net'
EMAIL_HOST              = 'localhost'
OPENID_RETURN           = 'http://www.fuzztrees.net/login/?openidreturn'

DATABASES = {
    'default': {
        #TODO: rename database to 'FuzzEd'?
        'ENGINE':   'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     'fuzztrees',                              # Or path to database file if using sqlite3.
        'USER':     'fuzztrees',                              # Not used with sqlite3.
        'PASSWORD': 'fuzztrees',                              # Not used with sqlite3.
        'HOST':     '',                                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     '',                                       # Set to empty string for default. Not used with sqlite3.
    }
}


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT+'/static-release/img',
)
ANALYZE_TOP_EVENT_PROBABILITY_SERVER = 'http://t420.asg-platform.org:8080'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    }, 
    'handlers': {
        'mail_admins': {
            'level':   'ERROR',
            'class':   'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers':  ['mail_admins'],
            'level':     'ERROR',
            'propagate': True,
        },
        'FuzzEd': {
            'handlers':  ['mail_admins'],
            'level':     'ERROR',
            'propagate': True,
        }
    }
}
