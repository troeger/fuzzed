from configurations import Configuration, values
import os.path


class Common(Configuration):
    AUTH_PROFILE_MODULE = 'FuzzEd.UserProfile'
    CORS_ORIGIN_ALLOW_ALL = True
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
    SERVER_EMAIL = values.Value('NOT_SET', environ_prefix='FUZZED')
    SITE_ID = 1
    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['next', ]
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_TWITTER_KEY = values.Value('NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_TWITTER_SECRET = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_LIVE_CLIENT_ID = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_LIVE_CLIENT_SECRET = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_YAHOO_OAUTH2_KEY = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_GITHUB_KEY = values.Value('NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_GITHUB_SECRET = values.Value(
        'NOT_SET', environ_prefix='FUZZED')
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        # Transition to 0.7.0 installation for existing users
        'social_core.pipeline.social_auth.associate_by_email',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details'
    )

    STATICFILES_DIRS = ('FuzzEd/static',)
    STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'
    STATIC_ROOT = 'FuzzEd/static-release/'
    STATIC_URL = '/static/'
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TIME_ZONE = 'UTC'      # setting this to None doesn't work on fresh Linux systems
    USE_I18N = False
    USE_L10N = True
    USE_TZ = False
    WSGI_APPLICATION = 'FuzzEd.wsgi.application'
    ROBOTS_USE_SITEMAP = False

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATES = [
        {
            'APP_DIRS': True,
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'context_processors': (
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect'
                )
            }
        },
    ]

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
        'django.contrib.sites',
        'robots',
        'require',
        'social_django',
        'tastypie',
        'FuzzEd'
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.twitter.TwitterOAuth',
        'social_core.backends.yahoo.YahooOAuth2',
        'social_core.backends.open_id.OpenIdAuth',
        'social_core.backends.live.LiveOAuth2',
        'social_core.backends.github.GithubOAuth2'
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
            'django.request': {},
            'FuzzEd': {}
        }
    }


class Dev(Common):
    DEBUG = True
    SECRET_KEY = "4711"
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
    TEMPLATES = Common.TEMPLATES
    TEMPLATES[0]['DIRS'] = ('FuzzEd/templates', 'FuzzEd/static/img')
    BACKEND_DAEMON = values.Value(
        'http://localhost:8001', environ_prefix='FUZZED')
    TERMS_PAGE = '/about/'
    FEEDBACK_PAGE = 'http://fuzzed.uservoice.com'
    FOOTER = 'FuzzEd Development Team (Dev Server)'
    SOCIAL_AUTH_USERNAME_FORM_URL = '/'
    SOCIAL_AUTH_USERNAME_FORM_HTML = 'dev_login.html'
    AUTHENTICATION_BACKENDS = Common.AUTHENTICATION_BACKENDS + \
        ('social_core.backends.username.UsernameAuth',)
    INTERNAL_IPS = (
        '0.0.0.0',
        '127.0.0.1',
    )
    LOGGING = Common.LOGGING
    LOGGING['loggers']['django.request']['handlers'] = ['console']
    LOGGING['loggers']['FuzzEd']['handlers'] = ['console']


class Production(Common):
    DEBUG = False
    SECRET_KEY = values.SecretValue(environ_prefix='FUZZED')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': values.Value('fuzzed', environ_prefix='FUZZED'),
            'USER': values.Value('fuzzed', environ_prefix='FUZZED'),
            'PASSWORD': values.Value('fuzzed', environ_prefix='FUZZED'),
            'HOST': values.Value('localhost', environ_prefix='FUZZED'),
            'PORT': values.Value('', environ_prefix='FUZZED'),
        }
    }
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ADMINS = (('FuzzEd Admin', str(values.Value(
        'xxx', environ_prefix='FUZZED', environ_name='ADMIN_EMAIL'))),)
    ALLOWED_HOSTS = [
        str(values.Value('xxx', environ_prefix='FUZZED', environ_name='SERVER'))]
    SERVER = str(values.Value(
        'xxx', environ_prefix='FUZZED', environ_name='SERVER_URL'))
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    TEMPLATES = Common.TEMPLATES
    #TEMPLATES[0]['DIRS'] = (PROJECT_ROOT + '/templates', PROJECT_ROOT + '/static-release/img')

    LOGGING = Common.LOGGING
    LOGGING['loggers']['django.request']['handlers'] = ['mail_admins']
    LOGGING['loggers']['FuzzEd']['handlers'] = ['file']
    # TODO: Ansible integration
    BACKEND_DAEMON = values.Value(
        'http://localhost:8001', environ_prefix='FUZZED')
    TERMS_PAGE = values.Value('/about/', environ_prefix='FUZZED')
    FEEDBACK_PAGE = values.URLValue(
        'http://fuzzed.uservoice.com', environ_prefix='FUZZED')
    FOOTER = values.Value('FuzzEd Development Team', environ_prefix='FUZZED')
