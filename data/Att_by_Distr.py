import datetime
import mongoengine



class Att_by_Distr(mongoengine.Document):

    district = mongoengine.StringField(required=True)

    attendance = mongoengine.StringField(required=True)

    enrol = mongoengine.IntField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'att_by_dist'
    }