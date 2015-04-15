from configurations import Configuration, values
import os.path
import logging


class Common(Configuration):
    AUTH_PROFILE_MODULE = 'FuzzEd.UserProfile'
    CORS_ORIGIN_ALLOW_ALL = True
    DJIKI_AUTHORIZATION_BACKEND = 'FuzzEd.wiki.FuzzEdWikiAccess'
    DJIKI_IMAGES_PATH = 'wiki_img'
    DJIKI_PARSER = 'FuzzEd.wiki'
    EMAIL_HOST = 'localhost'
    EMAIL_SUBJECT_PREFIX = '[FuzzEd] '
    LANGUAGE_CODE = 'en-en'
    LOGIN_REDIRECT_URL = '/projects/'
    LOGIN_URL = '/'
    REQUIRE_BASE_URL = 'script'
    REQUIRE_BUILD_PROFILE = '../lib/requirejs/require_build_profile.js'
    REQUIRE_JS = '../lib/requirejs/require-jquery.js'
    ROOT_URLCONF = 'FuzzEd.urls'
    MEDIA_ROOT = ''
    MEDIA_URL = ''
    SEND_BROKEN_LINK_EMAILS = False
    SERVER_EMAIL = values.Value(
        'webmaster@fuzzed.org',
        environ_name='FUZZED_ADMIN_EMAIL')
    SITE_ID = 1
    SOCIAL_AUTH_URL_NAMESPACE = 'social'
    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['next',]
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '589443374752-dsq0s0u2uivo8f8edviimou2p97k2ii8.apps.googleusercontent.com'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Y2kEQk7JHyHTUeH4sLZQIhRA'
    SOCIAL_AUTH_TWITTER_KEY = 'k2MzFngdzZTEBLs2E4A7zqhs7'
    SOCIAL_AUTH_TWITTER_SECRET = 'Y9XauAcebgNpnf0czIH834oCyNTPxvJz872xmz1EPGulXK6nUh' 
    SOCIAL_AUTH_LIVE_CLIENT_ID = ''
    SOCIAL_AUTH_LICE_CLIENT_SECRET = '' 
    SOCIAL_AUTH_YAHOO_OAUTH2_KEY = 'dj0yJmk9TFltelp2Q1hIaUlCJmQ9WVdrOVoyTmhRVFpPTm1jbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1mMA--'
    SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = 'cd77daf8e9952eee6cf7d5af0b4a52b6c5b6926f'


    STATICFILES_DIRS = ('FuzzEd/static',)
    STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'
    STATIC_ROOT = 'FuzzEd/static-release/'
    STATIC_URL = '/static/'
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TIME_ZONE = None
    USE_I18N = False
    USE_L10N = True
    USE_TZ = False
    WSGI_APPLICATION = 'FuzzEd.wsgi.application'

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.static',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'social.apps.django_app.context_processors.backends',
        'social.apps.django_app.context_processors.login_redirect'       
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'FuzzEd.middleware.HttpErrorMiddleware',
    )

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'require',
        'social.apps.django_app.default',        
        'tastypie',
        'djiki',
        'FuzzEd'
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'social.backends.google.GoogleOAuth2',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.yahoo.YahooOAuth2',
        'social.backends.open_id.OpenIdAuth',
        'social.backends.live.LiveOAuth2'
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
                'level': 'DEBUG',
                'class': 'logging.StreamHandler'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/tmp/fuzzed.log',
            },
            'False': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'FuzzEd': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            }
        }
    }


class Dev(Common):
    DEBUG = True
    TEMPLATE_DEBUG = True
    SECRET_KEY = 'kjshdgfiu438o374o38g4o8figwilfuz4iou34gli'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'fuzzed.sqlite',
            'USER': 'fuzzed.sqlite',
            'PASSWORD': 'fuzzed',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    TEST = {'NAME': 'test_fuzzed.sqlite'}
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SERVER = 'http://localhost:8000'
    OPENID_RETURN = SERVER + '/login/?openidreturn'
    TEMPLATE_DIRS = ('FuzzEd/templates',
                     'FuzzEd/static/img',
                     'FuzzEd/templates/djiki',
                     'djiki')
    BACKEND_DAEMON = "http://localhost:8000"
    TERMS_PAGE = '/about/'
    FEEDBACK_PAGE = 'http://fuzzed.uservoice.com'
    FOOTER = 'FuzzEd Development Team (Dev Server)'


class Vagrant(Dev):
    SERVER = 'http://192.168.33.10:8000'
    OPENID_RETURN = 'http://192.168.33.10:8000/login/?openidreturn'
    FOOTER = 'FuzzEd Development Team (Vagrant Server)'


class Production(Common):
    DEBUG = False
    TEMPLATE_DEBUG = False
    # Using values.SecretValue here breaks the Dev configuration
    SECRET_KEY = values.Value('837dsfskfjh!',
                              environ_name='FUZZED_SECRET')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': values.Value('fuzzed',
                                 environ_name='FUZZED_DB_NAME'),
            'USER': values.Value('fuzzed',
                                 environ_name='FUZZED_DB_USER'),
            'PASSWORD': values.Value('fuzzed',
                                     environ_name='FUZZED_DB_PW'),
            'HOST': values.Value('localhost',
                                 environ_name='FUZZED_DB_HOST'),
            'PORT': values.Value('',
                                 environ_name='FUZZED_DB_PORT'),
        }
    }
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ALLOWED_HOSTS = [values.Value('fuzzed.org',
                                  environ_name='FUZZED_HOST_NAME')]
    SERVER = 'https://' + str(values.Value('fuzzed.org',
                                           environ_name='FUZZED_HOST_NAME'))
    OPENID_RETURN = SERVER + '/login/?openidreturn'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIRS = (PROJECT_ROOT + '/templates',
                     PROJECT_ROOT + '/static-release/img',
                     PROJECT_ROOT + '/templates/djiki')
    LOGGING = Common.LOGGING
    LOGGING['loggers']['django.request']['handlers'] = ['mail_admins']
    LOGGING['loggers']['FuzzEd']['handlers'] = ['file']
    BACKEND_DAEMON = values.Value('http://example.com:8000',
                                  environ_name='FUZZED_BACKEND_HOST_NAME')
    TERMS_PAGE = values.Value('/about/',
                              environ_name='FUZZED_TERMS_PAGE')
    FEEDBACK_PAGE = values.URLValue('http://example.com',
                                    environ_name='FUZZED_FEEDBACK_PAGE')
    FOOTER = values.Value('FuzzEd Development Team',
                          environ_name='FUZZED_FOOTER')
