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
