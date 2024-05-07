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
