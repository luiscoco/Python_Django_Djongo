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
