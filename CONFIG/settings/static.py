from .base import BASE_DIR

STATIC_URL = '/static/'

# Directories for local static files (optional)
STATICFILES_DIRS = [
    BASE_DIR / "static",  # assuming BASE_DIR is the root directory of your project
    # Other directories can be added here
]

# Not needed for local development, but typically used in production
# STATIC_ROOT = BASE_DIR / 'staticfiles'
