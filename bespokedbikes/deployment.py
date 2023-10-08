import os 
from .settings import *
from .settings import BASE_DIR


SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['bespoked-bikes.azurewebsites.net', 
                 'www.bespoked-bikes.azurewebsites.net', 
                 '169.254.129.5', 
                 '0.0.0.0', 
                 '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['bespoked-bikes.azurewebsites.net', 
                        'www.bespoked-bikes.azurewebsites.net', 
                        '169.254.129.5', 
                        '0.0.0.0', 
                        '127.0.0.1']
DEBUG = False

# WhiteNoise configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] 

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
print(conn_str_params)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME'),
        'HOST': os.environ.get('DBHOST'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}