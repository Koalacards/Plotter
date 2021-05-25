import json
from typing import Dict, List
import discord
import random
import db.plotdbfunctions as dbfunc

def str2dict(dict_str: str) -> Dict:
    json_compatible = dict_str.replace("'", "\"")
    new_dict = json.loads(json_compatible)
    return new_dict

def str2numlist(numlist_str: str) -> List[float]:
    try:
        num_list = [ float(x) for x in numlist_str.split() ]
        return num_list
    except Exception as e:
        pass
    try:
        num_list = [ float(x) for x in numlist_str.split(", ") ]
        return num_list
    except Exception as e:
        pass

    try:
        num_list = [ float(x) for x in numlist_str.split(",") ]
        return num_list
    except Exception as e:
        pass

    raise Exception("Either the format is bad or one of the values is not a number")


def str2strlist(strlist_str: str) -> List[str]:
    try:
        str_list = [ str(x) for x in strlist_str.split() ]
        return str_list
    except Exception as e:
        print(e)
        pass
    try:
        str_list = [ str(x) for x in strlist_str.split(", ") ]
        return str_list
    except Exception as e:
        print(e)
        pass

    try:
        str_list = [ str(x) for x in strlist_str.split(",") ]
        return str_list
    except Exception as e:
        print(e)
        pass

    raise Exception("The format is bad")

def verify_list_is_numlist(potential_numlist):
    for num in potential_numlist:
        if type(num) != float:
            return None
    
    return True

def create_embed(title:str, description:str, color) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        colour=color
    )
    return embed

def error_embed(description:str) -> discord.Embed:
    return create_embed("Plotter Error", description, discord.Color.red())

def random_num_list(amount:int, min:float, max:float) -> List[float]:
    try:
        min = float(min)
        max = float(max)
    except:
        raise Exception("min or max is not a float")
    random_list=[]
    for _ in range(amount):
        random_list.append(round(random.uniform(min, max), 3))
    return random_list

#Check if the axis info is boundaries or one of the options, and return either a list or string depending
def sanitize_axis_info(author, dataset_name:str):
    axis_str = dbfunc.get_axis_info(author.id, dataset_name)
    axis_load = json.loads(axis_str)
    if type(axis_load) == list:
        return axis_load
    else:
        return str(axis_load)
