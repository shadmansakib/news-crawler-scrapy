from datetime import datetime

from mongoengine import DynamicDocument, StringField, DateTimeField, ListField, URLField


class News(DynamicDocument):
    heading = StringField()
    author = StringField()
    details = StringField()
    image = URLField()
    news_url = URLField(unique=True)

    categories = ListField(StringField())
    tags = ListField(StringField())
    excerpt = StringField()

    publisher = StringField()
    language = StringField()

    # UTC datetime
    publish_time = DateTimeField()
    last_update_time = DateTimeField()

    created_on = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'news',
        'ordering': ['-publish_time'],
    }
