# Python a CRUD API with Django and Djongo (MongoDB database)

Creating a **Django CRUD API** application with **MongoDB** as the database backend and including **Swagger** for **OpenAPI documentation** involves several steps

Here's a guide to set up the application:

## 1. Set up Your Environment

Make sure you have Python and pip installed. You can then create a virtual environment and activate it:

```
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
```

## 2. Install Required Packages

Install **Django**, **djongo** (a tool that allows **Django** to use **MongoDB** as the backend), and packages for **Swagger** documentation:

```
pip install django djangorestframework djongo drf-yasg
```

## 3. Create a New Django Project

Create a new **Django** project and a new application within it:

```
django-admin startproject myproject
cd myproject
python manage.py startapp myapp
```

## 4. Configure MongoDB in settings.py

In your **settings.py**, configure the database to use Djongo which connects **Django** to **MongoDB**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'your-database-name',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'your-mongodb-uri'
        }
    }
}
```

Also, add the created app and other necessary Django extensions to **INSTALLED_APPS**:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'myapp',
]
```

## 5. Create a Model

In **myapp/models.py**, define a model:

```python
from djongo import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
```

## 6. Create Serializers

In **myapp/serializers.py**, create serializers for your models:

```python
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
```

## 7. Create Views

In **myapp/views.py**, use **Django REST** Framework's viewsets for CRUD operations:

```python
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

## 8. Configure URLs

In **myproject/urls.py**, set up URL routing for both the application and the **Swagger** documentation:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from myapp.views import ItemViewSet

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Item API",
      default_version='v1',
      description="API for CRUD operations on items",
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```

## 9. Run Migrations and Start the Server

Finally, run migrations and start your Django server:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

You can now access the **Swagger** documentation at **http://127.0.0.1:8000/swagger/** to interact with your API

This setup provides you with a **Django** application configured to perform **CRUD** operations on **MongoDB** with **OpenAPI** documentation provided through **Swagger**
