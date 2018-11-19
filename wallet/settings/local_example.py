"""
These settings overrides the ones in settings/base.py
"""

SECRET_KEY = 'somestring'
# you can also use environment variables to store secret values
# import os
# SECRET_KEY = os.environ['SECRET_KEY']


CLIENT_AUTH_BASE = "http://localhost:3000"

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': CLIENT_AUTH_BASE + '/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': CLIENT_AUTH_BASE + '/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user': 'base.serializers.UserSerializer'
    },
}

# input local postgres server details here
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
"""
