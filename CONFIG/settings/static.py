from .base import BASE_DIR
import os

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directories for local static files (optional)
STATICFILES_DIRS = [
    BASE_DIR / "static",  # assuming BASE_DIR is the root directory of your project
    # Other directories can be added here
]

# Not needed for local development, but typically used in production
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# This is for serving static files in production
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Enable WhiteNoise to compress files and serve efficiently
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'