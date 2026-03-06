import os
from django.core.wsgi import get_wsgi_application

# This points to your settings file in the movie_project folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_project.settings')

application = get_wsgi_application()