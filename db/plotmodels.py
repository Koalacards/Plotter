from peewee import *

database = SqliteDatabase('db/plotdata.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class DatasetEntries(BaseModel):
    axis_info = TextField(null=True)
    data = TextField(null=True)
    ds_name = TextField(null=True)
    graph_data = TextField(null=True)
    plot_title = TextField(null=True)
    user_id = IntegerField(null=True)
    x_ticks = TextField(null=True)
    y_ticks = TextField(null=True)
    legend = TextField(null=True)

    class Meta:
        table_name = 'DatasetEntries'
        primary_key = False

