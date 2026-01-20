import mongoengine

def init_db(app):
    mongoengine.connect(
        db=app.config['MONGO_DBNAME'],
        host=app.config['MONGO_URI'],
        username=app.config.get('MONGO_USERNAME'),
        password=app.config.get('MONGO_PASSWORD'),
        authentication_source='admin'  # Change if your user is in another DB
    )
