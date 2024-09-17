import os, sys
from django.contrib.messages import constants as messages
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "..", "..", "apps"))

SECRET_KEY = 'django-insecure-&a@s(za*td#ph@ja=vz&k4b=127su)x+#&h%l@i(jnb_w-br_%'

DEBUG = True
ALLOWED_HOSTS = ['*']
# INTERNAL_IPS=['127.0.0.1']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'IS_Nexus',
    'IntelliSync_db',
    'Payroll_db',
    'AccessArmor',
    'HRMS_db',
    'ESS',
    'ATE'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "IS_Nexus.middleware.SuperuserMiddleware",
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
                'IS_Nexus.context.main_menu',
                'IS_Nexus.context.user_permission',
            ],
        },
    },
]

WSGI_APPLICATION = 'MAIN.wsgi.application'

current_year_list=[
    int(str(datetime.now().year)[-2:]),
    int(str(datetime.now().year)[-2:])-1
    # int(str(datetime.now().year)[-2:])-2
]

DATABASES = {
    'default': {
        'ENGINE' : 'mssql',
        'NAME': 'IS_HRIMS_db',
        'USER': 'sa',
        'PASSWORD': 'Admin@123',
        'HOST': '97.74.81.103',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    'intellisync_db': {
        'ENGINE' : 'mssql',
        'NAME': 'is_intellisync_db',
        'USER': 'sa',
        'PASSWORD': 'Admin@123',
        'HOST': '97.74.81.103',
        'OPTIONS': {'driver': 'ODBC Driver 17 for SQL Server',},
    },
    # 'payroll_db':{
    #     'ENGINE':'mssql',
    #     'NAME':f'om_01_23',
    #     'USER':'sa',
    #     'PASSWORD':'Admin@123',
    #     'HOST':'97.74.81.103',
    #     'OPTIONS':{'driver': 'ODBC Driver 17 for SQL Server',}
    # }
}


for current_year in current_year_list:
    DATABASES[f'payroll_db_{current_year}']={
        'ENGINE':'mssql',
        'NAME':f'om_01_{current_year}',
        'USER':'sa',
        'PASSWORD':'Admin@123',
        'HOST':'97.74.81.103',
        'OPTIONS':{'driver': 'ODBC Driver 17 for SQL Server',}
    }


AUTH_PASSWORD_VALIDATORS = [
    # { 'NAME' : 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    # { 'NAME' : 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    # { 'NAME' : 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    # { 'NAME' : 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ************ Custom Settings ************

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

# Data base routers
DATABASE_ROUTERS = [
    'router.IntelliSyncDbRouter',
    'router.PayrollDbRouter',
    'router.HRMSDbRouter'
]

PROJECT_CODE = 'is_hrms'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.qlc.co.in'
EMAIL_HOST_USER = 'hralert@globalfashionindia.com'
EMAIL_HOST_PASSWORD = 'zns#a2@792'
# EMAIL_HOST = 'mail.ss-creations.in'
# EMAIL_HOST_USER = 'implementation@ss-creations.in'
# EMAIL_HOST_PASSWORD = 'Admin@123'
EMAIL_PORT = 587
