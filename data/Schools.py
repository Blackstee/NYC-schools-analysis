import datetime
import mongoengine


class Schools(mongoengine.Document):

    dbn =  mongoengine.StringField(required=True)

    name = mongoengine.StringField(required=True)

    num_takers = mongoengine.StringField(required=True)

    reading_score = mongoengine.StringField(required=True)

    math_score = mongoengine.StringField(required=True)

    writing_score = mongoengine.StringField(required=True)

    num_takers2 = mongoengine.StringField(required=True)

    exam_taken2 = mongoengine.StringField(required=True)

    exam_good2 = mongoengine.StringField(required=True)

    Form_ids = mongoengine.ListField()

    avg_score = mongoengine.IntField(required=True)


    meta = {
        'db_alias': 'core',
        'collection': 'schools'
    }