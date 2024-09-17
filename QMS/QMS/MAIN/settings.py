import os, sys
from django.contrib.messages import constants as messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "..", "..", "apps"))

SECRET_KEY = 'django-insecure-&a@s(za*td#ph@ja=vz&k4b=127su)x+#&h%l@i(jnb_w-br_%'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'IS_Nexus',
    'IntelliSync_db',
    'Payroll_db',
    'ERP_db',
    'QMS_db',
    'AccessArmor',
    'RTQM',
    'EndLine',
    # 'Masters',
    "corsheaders",
    'rest_framework',
    
]

MIDDLEWARE = [
     "corsheaders.middleware.CorsMiddleware",
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "IS_Nexus.middleware.SuperuserMiddleware"
]

ROOT_URLCONF = 'MAIN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'IS_Nexus.context.main_menu'
            ],
        },
    },
]

WSGI_APPLICATION = 'MAIN.wsgi.application'


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'QMS_db', 
    #     'USER': 'sa',
    #     'PASSWORD': 'jadon123',
    #     'HOST': 'localhost', 
    #     'PORT': '5432',
    # },
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'QMS_db', 
        'USER': 'sa',
        'PASSWORD': 'Admin@123',
        'HOST': '103.190.95.164', 
        'PORT': '5432',
    },
    'intellisync_db': {
        'ENGINE' : 'mssql',
        'NAME': 'is_intellisync_db',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': 'SSCREATION\\ISSQLSERVER',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
     'is_app_db': {
        'ENGINE' : 'mssql',
        'NAME': 'is_app_db_new',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': 'SSCREATION\\ISSQLSERVER',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    'payroll_db' : {
        'ENGINE' : 'mssql',
        'NAME': 'om_01_24',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': 'SSCREATION\\ISSQLSERVER',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    'erp_db' : {
        'ENGINE' : 'mssql',
        'NAME': 'VisualGEMS',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': 'SSCREATION\\ISSQLSERVER',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME' : 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    { 'NAME' : 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    { 'NAME' : 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    { 'NAME' : 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# *********** Custom Settings ***********

# Indian Timezone
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Reconfigure Static and Media Files Access
ASSETS_DIR = os.path.join(BASE_DIR, '..', '..', 'assets')
STATICFILES_DIRS = [ASSETS_DIR + '/static']
STATIC_URL = 'static/'
STATIC_ROOT = ASSETS_DIR + '/staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = ASSETS_DIR + '/media'

# Session 
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 36000 # Session timeout 60*60*10 = 10 Hours

# Redirect to this url if user is not logged in
LOGIN_URL = '/login/'

# Custom User Model
AUTH_USER_MODEL = 'IntelliSync_db.User'

# Customize alert message type
MESSAGE_TAGS = {
    messages.ERROR: 'error',
    messages.SUCCESS: 'success',
    messages.INFO: 'info',
    messages.WARNING : 'warning'
}

DATABASE_ROUTERS = [
    'router.AppDbRouter', 
    'router.IntelliSyncDbRouter', 
    'router.HRMSDbRouter', 
    'router.PayrollDbRouter', 
    'router.ERPDbRouter',
    'router.QMSDbRouter'
]

PROJECT_CODE = 'is_QMS'




# ===================>

# Frontend Connection

 
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
   "http://103.190.95.164:11005",
   "http://localhost:11005",
]

CSRF_TRUSTED_ORIGINS = [
    "http://103.190.95.164:11005",
    "http://localhost:11005",
]
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.example\.com$",
# ]

CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    # "DELETE",
    # "OPTIONS",
    # "PATCH",
    # "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)


