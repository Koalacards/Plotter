import json

def str2dict(dict_str: str):
    json_compatible = dict_str.replace("'", "\"")
    new_dict = json.loads(json_compatible)
    return new_dict

def str2numlist(numlist_str: str):
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


def str2strlist(strlist_str: str):
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