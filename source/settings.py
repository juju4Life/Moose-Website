
import os

from celery.schedules import crontab
import cloudinary
from decouple import config

# Configuration for Cloudinary, Image hosting through Heroku. Only used site images and not products
cloudinary.config(
    cloud_name=config('CLOUDINARY_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),

                  )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Ceery configuration
celery_broker_url = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'task-update-key': {
        'task': 'customer.tasks.update_tcg_key',
        'schedule': crontab(hour='5', minute='0', day_of_week='1'),
    },

}

EMAIL_USE_TLS = True
EMAIL_HOST = config('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = config('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = config('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = config('MAILGUN_SMTP_PORT')


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = [
                'smiling-earth.herokuapp.com', 'localhost', '127.0.0.1', 'www.tcgfirst.com',

]

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'engine',
    'orders',
    'orders.apps.OrderConfig',
    'django.contrib.admin',
    'engine.apps.EngineConfig',
    'contact',
    'contact.apps.ContactConfig',
    'buylist',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'simple_history',
    'django_celery_results',
    'django_celery_beat',
    'debug_toolbar',
    'customer',
    'customer.apps.CustomerConfig',
    'sms',
    'rest_framework',
    'import_export',
    'tcg',
    'paypal.standard.ipn',
    'ppal',
    'amazon',
    'captcha',
    'layout',
    'layout.apps.LayoutConfig',
    'cloudinary',
    'mail',
    'administration',
    'administration.apps.AdministrationConfig',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_KEY_PREFIX = ''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

ROOT_URLCONF = 'source.urls'

PROJECT_DIR = os.path.dirname(__file__)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['engine/templates', 'customer/templates', 'users/templates',
                'users/templates/registration', 'orders/templates', 'administration/templates'],

        'OPTIONS': {
            'loaders': ['admin_tools.template_loaders.Loader', 'django.template.loaders.app_directories.Loader'],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

)


WSGI_APPLICATION = 'source.wsgi.application'


DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': DB_HOST,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },


    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https', )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'media')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SITE_ID = 1

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'

DATA_UPLOAD_MAX_NUMBER_FIELDS = None
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_url = None

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'My subject: '
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_FORM_CLASS = None
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_PASSWORD_MIN_LENGTH = 6
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True


CART_SESSION_KEY = 'cart_id'
BUYLIST_CART_SESSION_KEY = 'buylist_cart_id'
PRODUCT_MODEL = "engine.MTG"
BUYLIST_MODEL = "engine.MTG"

INTERNAL_IPS = ('127.0.0.1', 'www.tcgfirst.com')

ADMIN_TOOLS_MENU = 'source.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'source.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'source.dashboard.CustomAppIndexDashboard'

