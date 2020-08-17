from mongoengine import connect, disconnect


def init_db():
    connect(
        db='news_crawler',
        # host='MONGODB_HOST',
        # port=MONGODB_PORT,
        # username='MONGODB_USERNAME',
        # password='MONGODB_PASSWORD',
        # authentication_source='admin',
    )


def disconnect_db():
    disconnect()
