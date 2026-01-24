import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medresearch.settings")

# Vercel requires 'app' or 'handler' variable
app = get_asgi_application()
application = app  # Keep for compatibility
