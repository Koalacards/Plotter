import peewee
from db.plotmodels import *


def set_dataset(user_id:int, name:str, ds_type:str):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id and DatasetEntries.name == name)
    if len(query) == 0:
        DatasetEntries.create(user_id=user_id, name=name, ds_type=ds_type, data="{}")
    else:
        raise Exception("Dataset already exists with user id and name")

def get_num_datasets(user_id:int):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id)
    return len(query)

def remove_dataset(user_id:int, name:str):
    query = DatasetEntries.delete().where(DatasetEntries.user_id == user_id and DatasetEntries.name == name)
    return query.execute()

        



