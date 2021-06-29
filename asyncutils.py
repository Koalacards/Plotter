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


async def get_saved_plot_dict(ctx, dataset_name:str, saved_plot_name:str):
    graph_dict = await get_graph_data_dictionary(ctx, dataset_name)

    #Get the saved plot dictionary or error if none is available
    saved_plot_dict = graph_dict.get(saved_plot_name, None)

    if saved_plot_dict is None:
        error_msg = f"You do not have a saved plot under the name {saved_plot_name}! Please check the name using `/viewgraphdata {dataset_name}` and try again."
        await ctx.send(embed=utils.error_embed(error_msg))
        return None

    return saved_plot_dict

async def get_saved_plot_type(ctx, dataset_name:str, saved_plot_name:str):
    graph_dict = await get_graph_data_dictionary(ctx, dataset_name)

    #Get the saved plot dictionary or error if none is available
    saved_plot_dict = graph_dict.get(saved_plot_name, None)

    if saved_plot_dict is None:
        error_msg = f"You do not have a saved plot under the name {saved_plot_name}! Please check the name using `/viewgraphdata {dataset_name}` and try again."
        await ctx.send(embed=utils.error_embed(error_msg))
        return None
    
    return saved_plot_dict["name"]


async def get_xticks_dictionary(ctx, dataset_name:str):
    author = ctx.author
    ticksstr = None
    #Recieve ticks data in string format from db
    try:
        ticksstr= dbfunc.get_x_ticks(author.id, dataset_name)
    except:
        description=f"You don't have a dataset with the name `{dataset_name}`!"
        await ctx.send(embed=utils.error_embed(description))
        return None

    #Turn ticks data in string format to dict format (this should only fail if the bot did something wrong)
    ticksdict = None
    try:
        ticksdict=utils.str2dict(ticksstr)
    except:
        description=f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return None

    return ticksdict

async def log_xticks_to_database(ctx, dataset_name:str, ticksdict) -> bool:
    author = ctx.author
    #add the new data to the database
    dict2str = str(ticksdict)
    try:
        dbfunc.set_x_ticks(author.id, dataset_name, dict2str)
    except:
        description=f"An error happened with the ticks data upload on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return False
    
    return True

async def get_yticks_dictionary(ctx, dataset_name:str):
    author = ctx.author
    ticksstr = None
    #Recieve ticks data in string format from db
    try:
        ticksstr= dbfunc.get_y_ticks(author.id, dataset_name)
    except:
        description=f"You don't have a dataset with the name `{dataset_name}`!"
        await ctx.send(embed=utils.error_embed(description))
        return None

    #Turn ticks data in string format to dict format (this should only fail if the bot did something wrong)
    ticksdict = None
    try:
        ticksdict=utils.str2dict(ticksstr)
    except:
        description=f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return None

    return ticksdict

async def log_yticks_to_database(ctx, dataset_name:str, ticksdict) -> bool:
    author = ctx.author
    #add the new data to the database
    dict2str = str(ticksdict)
    try:
        dbfunc.set_y_ticks(author.id, dataset_name, dict2str)
    except:
        description=f"An error happened with the ticks data upload on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return False
    
    return True
#Sanitize ticks info, x if x_or_y is true and y if x_or_y is false
async def sanitize_ticks_info(ctx, dataset_name:str, x_or_y:bool):
    ticks_dict = None
    if x_or_y:
        ticks_dict = await get_xticks_dictionary(ctx, dataset_name)
    else:
        ticks_dict = await get_yticks_dictionary(ctx, dataset_name)

    if ticks_dict is None:
        return None
    
    if ticks_dict == {}:
        return False
    else:
        answer = []
        answer.append(ticks_dict["ticks"])
        labels = ticks_dict.get("labels", None)
        if labels is not None:
            answer.append(labels)

        return answer

#Check if rows of values have the same length
async def verify_same_length(ctx, values, labels):
    labels_string = ", ".join(labels)
    if values == []: 
        description=f"An error happened on our end: Values list is empty. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
        await ctx.send(embed=utils.error_embed(description))
        return None
    
    first_length = len(values[0])

    for value in values:
        if len(value) != first_length:
            description=f"The following rows must have the same number of values: {labels_string}. Please change your input and try again."
            await ctx.send(embed=utils.error_embed(description))
            return None
    
    return True