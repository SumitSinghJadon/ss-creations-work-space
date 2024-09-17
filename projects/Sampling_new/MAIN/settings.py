import os, sys
from django.contrib.messages import constants as messages

from datetime import timedelta



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
    'Sampling_db',
    'IntelliSync_db',
    'Payroll_db',
    'ERP_db',
    'AccessArmor',
    'Reports',
    'PRODUCTION_NEW',
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt',
    'IS_erp_db'
   
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your_secret_key',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', 'rest_framework_simplejwt.tokens.RefreshToken'),

}


DATABASES = {
    'default' : {
        'ENGINE' : 'mssql',
        'NAME': 'is_sampling_db',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': '103.190.95.164,2599',
        'OPTIONS': { 'driver': 'ODBC Driver 17 for SQL Server', },
    },
    'intellisync_db': {
        'ENGINE' : 'mssql',
        'NAME': 'is_intellisync_db',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': '103.190.95.164,2599',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server', },
    },
    'payroll_db' : {
        'ENGINE' : 'mssql',
        'NAME': 'om_01_24',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': '103.190.95.164,2599',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    'erp_db' : {
        'ENGINE' : 'mssql',
        'NAME': 'VisualGEMS',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': '103.190.95.164,2599',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    'is_app': {
        'ENGINE' : 'mssql',
        'NAME': 'is_app_db_new',
        'USER': 'sa',
        'PASSWORD': 'Ssc@Admin#123',
        'HOST': '103.190.95.164,2599',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    'is_erpdb':{
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': 'is_erpdb',
        'USER': 'postgres',
        'PASSWORD': 'jadon123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
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
    'router.ISERPDbRouter'
]

PROJECT_CODE = 'is_sampling'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.ss-creations.in'
EMAIL_HOST_USER = 'implementation@ss-creations.in'
EMAIL_HOST_PASSWORD = 'Admin@123'
EMAIL_PORT = 587






CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


CSRF_TRUSTED_ORIGINS = [
   "http://localhost:5173",
   "http://127.0.0.1:5173"
]


SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600   # 2 weeks
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
SESSION_COOKIE_HTTPONLY = True  # Ensure session cookies are accessible only via HTTP
SESSION_COOKIE_SAMESITE = 'Lax' 


CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS =["http://127.0.0.1:5173"]
CSRF_COOKIE_SECURE =  False
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_SAMESITE = 'Lax'