import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

application = get_wsgi_application()
app = application  # Vercel-এর জন্য এটি যোগ করা জরুরি