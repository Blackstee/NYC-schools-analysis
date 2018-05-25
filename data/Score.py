import mongoengine


class Score(mongoengine.Document):

    name = mongoengine.StringField(required=True)

    score = mongoengine.IntField(required=True)


    meta = {
        'db_alias': 'core',
        'collection': 'scores'
    }