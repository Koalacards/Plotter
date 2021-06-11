import json
from typing import Dict, List
import discord
import random
import db.plotdbfunctions as dbfunc
from matplotlib import colors

def str2dict(dict_str: str) -> Dict:
    json_compatible = dict_str.replace("'", "\"")
    new_dict = json.loads(json_compatible)
    return new_dict

def str2numlist(numlist_str: str, separator:str) -> List[float]:
    try:
        num_list = [ float(x) for x in numlist_str.split(separator) ]
        return num_list
    except Exception as e:
        raise Exception("Either the format is bad or one of the values is not a number")


def str2strlist(strlist_str: str, separator:str) -> List[str]:
    try:
        str_list = [ str(x) for x in strlist_str.split(separator) ]
        return str_list
    except Exception as e:
        raise Exception("The format is bad")\

def str2colorlist(colorlist_str:str, separator:str) -> List[str]:
    colorlist = str2strlist(colorlist_str, separator)
    try:
        verify_list_is_colorlist(colorlist)
        return colorlist
    except:
        raise Exception("One of the colors in the list is not a hex color.")


def verify_string_is_color(colorstr:str):
    try:
        colors.hex2color(colorstr)
    except:
        raise Exception("Color is not a hex color!")

def generate_random_color():
    color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
    return color


def verify_list_is_numlist(potential_numlist):
    for num in potential_numlist:
        if type(num) != float:
            return None
    
    return True

def verify_list_is_colorlist(potential_colorlist):
    for color in potential_colorlist:
        try:
            verify_string_is_color(color)
        except:
            raise Exception("One of the colors in the list is not a hex color.")

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
