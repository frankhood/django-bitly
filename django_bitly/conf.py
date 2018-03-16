from django.conf import settings

BITLY_TIMEOUT = getattr(settings, 'BITLY_TIMEOUT', 5)
BITLY_API_VERSION = getattr(settings, 'BITLY_API_VERSION', "2.0.1")
