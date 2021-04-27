import peewee
from db.plotmodels import *


def set_dataset(user_id:int, ds_name:str):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id and DatasetEntries.ds_name == ds_name)
    if len(query) == 0:
        DatasetEntries.create(user_id=user_id, ds_name=ds_name, data="{}", plot_title=ds_name)
    else:
        raise Exception("Dataset already exists with user id and ds_name")

def get_num_datasets(user_id:int):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id)
    return len(query)

def remove_dataset(user_id:int, ds_name:str):
    query = DatasetEntries.delete().where(DatasetEntries.user_id == user_id and DatasetEntries.ds_name == ds_name)
    return query.execute()

def get_dataset_data(user_id:int, ds_name:str):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id and DatasetEntries.ds_name == ds_name)
    if len(query) == 0:
        raise Exception("No dataset exists with given ds_name")  
    else:
        for item in query:
            return item.data     

def set_dataset_data(user_id:int, ds_name:str, data:str):
    query = DatasetEntries.update(data=data).where(DatasetEntries.user_id == user_id and DatasetEntries.ds_name == ds_name)
    return query.execute()

def get_names_of_datasets(user_id:int):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id)
    return_str = "Datasets: \n"
    for item in query:
        return_str+= f"{item.ds_name} \n"
    return return_str

def set_plot_title(user_id:int, ds_name:str, plot_title:str):
    query=DatasetEntries.update(plot_title=plot_title).where(DatasetEntries.user_id == user_id and DatasetEntries.ds_name == ds_name)
    return query.execute()

def get_plot_title(user_id:int, ds_name:str):
    query = DatasetEntries.select().where(DatasetEntries.user_id == user_id and DatasetEntries.ds_name == ds_name)
    if len(query) == 0:
        raise Exception("No dataset exists with given ds_name")  
    else:
        for item in query:
            return item.plot_title 

