import mongoengine


class Student(mongoengine.Document):

    full_name = mongoengine.StringField(required=True)

    sex = mongoengine.StringField(required=True)

    scores_ids = mongoengine.ListField()

    avg_score = mongoengine.IntField(required=True)

    district = mongoengine.IntField(required=True)



    meta = {
        'db_alias': 'core',
        'collection': 'students'
    }