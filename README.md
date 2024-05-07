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

```python
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

## 8. Define the Views in the application

**myapp/views.py**

```python
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .db import items  # Import the items collection
from bson import ObjectId
import json


def convert_to_item_dict(item):
    """Convert _id to id and remove _id field."""
    item['id'] = str(item.pop('_id'))
    return item


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the item'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age of the item')
    },
    required=['name', 'age']
))
@api_view(['POST'])
@permission_classes([AllowAny])
def create_item(request):
    try:
        data = json.loads(request.body)
        item = {
            'name': data['name'],
            'age': data['age']
        }
        result = items.insert_one(item)
        item['_id'] = str(result.inserted_id)  # Convert _id to string here
        return JsonResponse(item, safe=False)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'Missing name or age in the request body'}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def read_items(request):
    items_list = list(items.find({}, {'_id': 1, 'name': 1, 'age': 1}))
    items_data = [convert_to_item_dict(item) for item in items_list]
    return JsonResponse({'items': items_data}, safe=False)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Updated name of the item'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated age of the item')
    }
))
@api_view(['POST'])
@permission_classes([AllowAny])
def update_item(request, item_id):
    data = json.loads(request.body)
    update_data = {key: data[key] for key in data if key in ['name', 'age']}
    result = items.update_one(
        {'_id': ObjectId(item_id)}, {'$set': update_data})
    return JsonResponse({'modified_count': result.modified_count})


@swagger_auto_schema(method='delete', manual_parameters=[
    openapi.Parameter('item_id', openapi.IN_PATH,
                      description="ID of the item to be deleted", type=openapi.TYPE_STRING)
])
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_item(request, item_id):
    result = items.delete_one({'_id': ObjectId(item_id)})
    return JsonResponse({'deleted_count': result.deleted_count})
```

## 9. Define the URLs in the project

**myproject/urls.py**

```python
from django.contrib import admin
from django.urls import path, include
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
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # Replace with your app name

    # Swagger and ReDoc URLs for API documentation
    path('swagger.json', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
```
