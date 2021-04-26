from peewee import *

database = SqliteDatabase('db/plotdata.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class DatasetEntries(BaseModel):
    data = TextField(null=True)
    ds_type = TextField(null=True)
    name = TextField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'DatasetEntries'
        primary_key = False

