import os
from .base import *
import dj_database_url

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    '^8ai-6gb!yyg19uangdahsi8a%c=)mb0xler7%0klh1mz!^snago;91_')

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = ['*']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'