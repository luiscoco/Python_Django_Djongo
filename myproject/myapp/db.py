from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DATABASE_NAME]
items = db['items']  # Define the items collection
