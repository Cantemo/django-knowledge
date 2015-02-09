import os

DIRNAME = os.path.dirname(__file__)

DEBUG = True

DATABASE_ENGINE = 'sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(DIRNAME, 'example.sqlite').replace('\\','/'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DIRNAME, 'static').replace('\\','/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DIRNAME, 'media').replace('\\','/')

INTERNAL_IPS = ('127.0.0.1',)

SITE_ID = 1
SECRET_KEY = 'lolz'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_nose',
    #'debug_toolbar',
    'knowledge',
    'django_coverage',
    'mock',
    'ckeditor',
)

ROOT_URLCONF = 'testapp.urls'

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(DIRNAME, 'reports').replace('\\','/')

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates').replace('\\','/'),
)

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Paragraph', 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ], 
    },
}


CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'
LOGIN_REDIRECT_URL = '/admin/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
