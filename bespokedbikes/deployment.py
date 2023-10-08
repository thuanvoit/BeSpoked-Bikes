import os 
from .settings import *
from .settings import BASE_DIR


print("run deploy")
SECRET_KEY = 'django-insecure-cx(rqcggbl*%_zk3_#x+!_je_a-kpztrr1%4^yzz%$&g0+-(!-'
print(f"SECRET_KEY: {SECRET_KEY}")
ALLOWED_HOSTS = ['bespoked-bikes.azurewebsites.net', 'www.bespoked-bikes.azurewebsites.net', '127.0.0.1', '000.00.00.00']
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
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
        'NAME': 'bespoked-bikes-database',
        'HOST': 'bespoked-bikes-server.postgres.database.azure.com',
        'USER': 'vioushqhxy',
        'PASSWORD': '3VVV3CN8285265XQ$',
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}