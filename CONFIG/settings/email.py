DEFAULT_FROM_EMAIL = "rojitech9@gmail.com"

ADMINS = [
    ("ROJITECH", "rojitech@gmail.com"),
]


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525
