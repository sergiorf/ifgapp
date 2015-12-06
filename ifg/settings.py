# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from os.path import abspath, dirname, join

PROJECT_PATH = abspath(dirname(__file__))
PROJECT_NAME = PROJECT_PATH.split('/')[-1]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xavi7u0#(fpl3g2whwun9p1aj9#rs@ehxn$5#rb@$c+&6ipih@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    # 'django.contrib.messages.context_processors.messages',
)

# Application definition

INSTALLED_APPS = (
    'pagination',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
   # 'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom:
    'autocomplete_light',
    'smart_selects',
    'ifgapp'
)

MIDDLEWARE_CLASSES = (
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
   # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ifg.urls'

WSGI_APPLICATION = 'ifg.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ifgapp',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#arquivos estaticos do projeto
STATICFILES_DIRS = ('',
    os.path.join(os.path.dirname(BASE_DIR), "static", "static_dirs")
)

# Onde os arquivos serao coletados
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static_root")

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
MODEL_DOC_ROOT = os.path.join('model', 'documents')
MEDIA_URL = '/media/'