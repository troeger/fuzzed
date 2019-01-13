from configurations import Configuration, values
import os.path


class Common(Configuration):
    BACKEND_DAEMON = values.Value(
        'http://back:8000', environ_prefix='ORE')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': values.Value('ore', environ_name='DB_NAME', environ_prefix='ORE'),
            'USER': values.Value('ore', environ_name='DB_USER', environ_prefix='ORE'),
            'PASSWORD': values.Value('ore', environ_name='DB_PASSWORD', environ_prefix='ORE'),
            'HOST': values.Value('localhost', environ_name='DB_HOST', environ_prefix='ORE'),
            'PORT': values.Value('', environ_name='DB_PORT', environ_prefix='ORE'),
        }
    }
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', values.Value('xxx', environ_prefix='ORE', environ_name='SERVER')]
    SERVER = str(values.Value(
        'xxx', environ_prefix='ORE', environ_name='SERVER_URL'))
    FEEDBACK_PAGE = values.URLValue(
        'https://groups.google.com/forum/#!forum/ore-support', environ_prefix='ORE')
    TERMS_PAGE = values.Value('/about/', environ_prefix='ORE')
    AUTH_PROFILE_MODULE = 'ore.UserProfile'
    CORS_ORIGIN_ALLOW_ALL = True
    EMAIL_HOST = 'localhost'
    EMAIL_SUBJECT_PREFIX = '[ORE] '
    LANGUAGE_CODE = 'en-en'
    LOGIN_REDIRECT_URL = '/projects/'
    LOGIN_URL = '/'
    REQUIRE_BASE_URL = 'script'
    REQUIRE_BUILD_PROFILE = '../lib/requirejs/require_build_profile.js'
    REQUIRE_JS = '../lib/requirejs/require-jquery.js'
    ROOT_URLCONF = 'ore.urls'
    MEDIA_ROOT = ''
    MEDIA_URL = ''
    USE_X_FORWARDED_HOST = True
    SEND_BROKEN_LINK_EMAILS = False
    SERVER_EMAIL = values.Value('NOT_SET', environ_prefix='ORE')
    SITE_ID = 1
    SOCIAL_AUTH_URL_NAMESPACE = 'social'
    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['next', ]
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_TWITTER_KEY = values.Value('NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_TWITTER_SECRET = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_LIVE_CLIENT_ID = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_LIVE_CLIENT_SECRET = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_YAHOO_OAUTH2_KEY = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_GITHUB_KEY = values.Value('NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_GITHUB_SECRET = values.Value(
        'NOT_SET', environ_prefix='ORE')
    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        # Transition to 0.7.0 installation for existing users
        'social.pipeline.social_auth.associate_by_email',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details'
    )

    STATICFILES_DIRS = ('ore/static',)
    STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'
    STATIC_ROOT = 'ore/static-release/'
    STATIC_URL = '/static/'
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TIME_ZONE = 'UTC'      # setting this to None doesn't work on fresh Linux systems
    USE_I18N = False
    USE_L10N = True
    USE_TZ = False
    WSGI_APPLICATION = 'ore.wsgi.application'
    ROBOTS_USE_SITEMAP = False

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.template.context_processors.debug',
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
        'ore.middleware.HttpErrorMiddleware',
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
        'social.apps.django_app.default',
        'tastypie',
        'ore'
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'social.backends.google.GoogleOAuth2',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.yahoo.YahooOAuth2',
        'social.backends.open_id.OpenIdAuth',
        'social.backends.live.LiveOAuth2',
        'social.backends.github.GithubOAuth2'
    )

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue'
            },
        },
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
            },
            'False': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
            'ore': {
                'handlers': ['console', ],
                'level': 'DEBUG',
                'propagate': True,
            },
            'social': {
                'handlers': ['console', ],
                'level': 'DEBUG',
                'propagate': True,
            },

        }
    }


class Dev(Common):
    DEBUG = True
    TEMPLATE_DEBUG = True
    SECRET_KEY = "4711"
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    TEMPLATE_DIRS = ('ore/templates',
                     'ore/static/img')
    FOOTER = 'ORE Development Team (Dev Server)'
    SOCIAL_AUTH_USERNAME_FORM_URL = '/'
    SOCIAL_AUTH_USERNAME_FORM_HTML = 'dev_login.html'
    AUTHENTICATION_BACKENDS = Common.AUTHENTICATION_BACKENDS + \
        ('social.backends.username.UsernameAuth',)
    LOGGING = Common.LOGGING
    LOGGING['loggers']['django.request']['handlers'] = ['console']
    LOGGING['loggers']['ore']['handlers'] = ['console']


class Production(Common):
    DEBUG = False
    TEMPLATE_DEBUG = False
    SECRET_KEY = values.SecretValue(environ_prefix='ORE')
    #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ADMINS = (('ORE Admin', str(values.Value(
        'xxx', environ_prefix='ORE', environ_name='ADMIN_EMAIL'))),)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIRS = (PROJECT_ROOT + '/templates',
                     PROJECT_ROOT + '/static-release/img')
    LOGGING = Common.LOGGING
    LOGGING['loggers']['django.request']['handlers'] = ['mail_admins']
    LOGGING['loggers']['ore']['handlers'] = ['console']
    FOOTER = values.Value('ORE Development Team', environ_prefix='ORE')
