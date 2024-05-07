# Python a CRUD API with Django and PyMongo (MongoDB database)

Creating a **Django CRUD API** application with **MongoDB** as the database backend and including **Swagger** for **OpenAPI documentation** involves several steps

Here's a guide to set up the application:

## 1. Set up Your Environment

Install the required libraries with pip:

```
pip install django djangorestframework drf-yasg pymongo
```

## 2. Create a new project and application

We first create the new project

```
django-admin startproject myproject
cd myproject
```

Then we create the new application

```
python manage.py startapp myapp
```

## 3. Configure PyMongo in your Django settings (settings.py)

We define the databases paramters:

```
# Database
# MongoDB settings
MONGO_DATABASE_NAME = 'mydatabase'
MONGO_URI = 'mongodb://localhost:27017/'
```

We also input the INSTALLED_APPS:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'myapp',  # Replace with your app name
]
```

This is the whole settings.py file:

**myproject/settings.py**

```python
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&7-vekbe_ge0d(9^pfzrpim$c%bp2datc$95$jki95sr#i*6eu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'myapp',  # Replace with your app name
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

ROOT_URLCONF = 'myproject.urls'  # Replace with your project name

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

# Replace with your project name
WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
# MongoDB settings
MONGO_DATABASE_NAME = 'mydatabase'
MONGO_URI = 'mongodb://localhost:27017/'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
```

## 4. Configure the database in the application

We create a new file db.py

**myapp/db.py**

```python
from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DATABASE_NAME]
items = db['items']  # Define the items collection
```

## 5. Create the data model

**myapp/models.py**

```python
from mongoengine import Document, StringField, IntField, connect

# Connect to MongoDB
connect('mydatabase', host='localhost', port=27017)


class Item(Document):
    name = StringField(required=True, max_length=200)
    age = IntField(required=True)

    def __str__(self):
        return f'{self.name} ({self.age})'
```

## 6. Serializers

**myapp/serializers.py**

```python
from rest_framework import serializers
from bson import ObjectId
from .db import items


class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()

    def create(self, validated_data):
        item = {
            'name': validated_data['name'],
            'age': validated_data['age']
        }
        result = items.insert_one(item)
        item['id'] = str(result.inserted_id)
        return item

    def update(self, instance, validated_data):
        update_data = {}
        if 'name' in validated_data:
            update_data['name'] = validated_data['name']
        if 'age' in validated_data:
            update_data['age'] = validated_data['age']
        result = items.update_one(
            {'_id': ObjectId(instance)}, {'$set': update_data})
        return instance

    def to_representation(self, instance):
        item = {
            'id': str(instance['_id']),
            'name': instance['name'],
            'age': instance['age']
        }
        return item
```

## 7. Define the URLs in the application

**myapp/urls.py**

```
from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Schema view setup for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Item API",
        default_version='v1',
        description="API documentation for Item management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API endpoints
    path('create-item/', views.create_item, name='create-item'),
    path('read-items/', views.read_items, name='read-items'),
    path('update-item/<str:item_id>/', views.update_item, name='update-item'),
    path('delete-item/<str:item_id>/', views.delete_item, name='delete-item'),

    # Swagger and ReDoc URLs for API documentation
    path('swagger.json', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
```

## 8. 
