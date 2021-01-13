from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['*']

DATABASES['default']['HOST'] = 'localhost'
DATABASES['default']['NAME'] = 'thetoyproject'
DATABASES['default']['USER'] = 'thetoyproject'
DATABASES['default']['PASSWORD'] = 'thetoyproject'