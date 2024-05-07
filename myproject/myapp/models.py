from mongoengine import Document, StringField, IntField, connect

# Connect to MongoDB
connect('mydatabase', host='localhost', port=27017)


class Item(Document):
    name = StringField(required=True, max_length=200)
    age = IntField(required=True)

    def __str__(self):
        return f'{self.name} ({self.age})'
