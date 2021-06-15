import utils
import db.plotdbfunctions as dbfunc
import plotvars

async def get_data_dictionary(ctx, dataset_name:str):
    author = ctx.author
    datastr = None
    #Recieve data in string format from db
    try:
        datastr= dbfunc.get_dataset_data(author.id, dataset_name)
    except:
        description=f"You don't have a dataset with the name `{dataset_name}`!"
        await ctx.send(embed=utils.error_embed(description))
        return None

    #Turn data in string format to dict format (this should only fail if the bot did something wrong)
    datadict = None
    try:
        datadict=utils.str2dict(datastr)
    except:
        description=f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return None

    return datadict

async def log_data_to_database(ctx, dataset_name:str, datadict) -> bool:
    author = ctx.author
    #add the new data to the database
    dict2str = str(datadict)
    try:
        dbfunc.set_dataset_data(author.id, dataset_name, dict2str)
    except:
        description=f"An error happened with the data upload on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return False
    
    return True


async def get_graph_data_dictionary(ctx, dataset_name:str):
    author = ctx.author
    graph_data_str = None
    #Recieve graph data in string format from db
    try:
        graph_data_str = dbfunc.get_dataset_graph_data(author.id, dataset_name)
    except:
        description=f"You don't have a dataset with the name `{dataset_name}`!"
        await ctx.send(embed=utils.error_embed(description))
        return None
    
    graph_data_dict = None
    try:
        graph_data_dict = utils.str2dict(graph_data_str)
    except:
        description=f"An error happened with the graph dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return None
    
    return graph_data_dict


async def log_graph_data_to_database(ctx, dataset_name:str, graph_data_dict) -> bool:
    author = ctx.author
    #add the new data to the database
    graph_dict2str = str(graph_data_dict)
    try:
        dbfunc.set_dataset_graph_data(author.id, dataset_name, graph_dict2str)
    except:
        description=f"An error happened with the graph data upload on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return False
    
    return True

async def verify_rows_exist_in_dataset(ctx, dataset_name:str, datadict, rows, send_error_message=True):
    row_values = []
    for row in rows:
        values = datadict.get(row, None)
        if values is None:
            if send_error_message:
                description = f"Row {row} does not exist in dataset {dataset_name}!"
                await ctx.send(embed=utils.error_embed(description))
            return None
        else:
            row_values.append(values)
    
    return row_values

async def verify_rows_are_rows_of_numbers(ctx, dataset_name:str, datadict, rows):

    row_values = await verify_rows_exist_in_dataset(ctx, dataset_name, datadict, rows)
    if row_values == None:
        return None
    
    for i in range (len(row_values)):
        verify_values=utils.verify_list_is_numlist(row_values[i])
        if verify_values is None:
            description= f"Row {rows[i]} is not a list of only numbers, which is required for a scatterplot. Please double-check the values using `/viewdata {dataset_name}` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return None
    
    return row_values


async def save_graph_data(ctx, dataset_name:str, saveas:str,  graph_data):
    #Get the pre-existing graph data
    graph_data_dict = await get_graph_data_dictionary(ctx, dataset_name)
    if graph_data_dict is None:
        return
    
    #Set the dictionary value for the saveas to be the graph data
    graph_data_dict[saveas] = graph_data

    #Write the graph data to the database
    graph_data_written = await log_graph_data_to_database(ctx, dataset_name, graph_data_dict)
    if graph_data_written == False:
        return
    

