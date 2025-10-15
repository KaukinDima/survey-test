#!/bin/bash
set -e

PROJECT_NAME="kostanay_map"
APP_NAME="analytics"

echo "🚀 Starting project setup: $PROJECT_NAME"

# 1. Create project folder
mkdir -p $PROJECT_NAME && cd $PROJECT_NAME

# 2. Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install django djangorestframework python-dotenv psycopg2-binary pandas openpyxl

# 4. Create Django project and app
django-admin startproject core .
django-admin startapp $APP_NAME

# 5. Create .env file
cat > .env <<EOF
DEBUG=True
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=kostanay_db
DB_USER=kostanay_user
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
EOF

# 6. Update settings.py
SETTINGS_FILE="core/settings.py"
echo "🛠  Patching $SETTINGS_FILE"

cat > $SETTINGS_FILE <<'PYCODE'
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
PYCODE

# 7. Create urls.py
cat > core/urls.py <<'PYCODE'
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('analytics.urls')),
]
PYCODE

# 8. Basic analytics/urls.py
cat > $APP_NAME/urls.py <<'PYCODE'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health'),
]
PYCODE

# 9. Basic analytics/views.py
cat > $APP_NAME/views.py <<'PYCODE'
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "message": "Kostanay Analytics backend is running"})
PYCODE

# 10. Run migrations
echo "🔧 Running migrations..."
python manage.py migrate

# 11. Create superuser prompt
echo "👤 Creating superuser (you can skip with Ctrl+C)..."
python manage.py createsuperuser || echo "Skipped superuser creation."

# 12. Run dev server
echo "🚀 Launching development server..."
python manage.py runserver 0.0.0.0:8000
