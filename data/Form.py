import mongoengine


class Form (mongoengine.Document):

    name =  mongoengine.StringField(required=True)

    Student_ids = mongoengine.ListField()

    avg_score = mongoengine.IntField(required=True)


    meta = {
        'db_alias': 'core',
        'collection': 'forms'
    }