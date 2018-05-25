import mongoengine


def global_init():
    mongoengine.register_connection(alias='core', name='snake_bnb', port=27018)
