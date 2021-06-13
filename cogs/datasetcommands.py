import discord
from discord.ext import commands
from discord_slash import cog_ext
import db.plotdbfunctions as dbfunc
import utils
import plotvars
from plotvars import guild_ids
import asyncutils
import os

class DataSetCommands(commands.Cog):
    @cog_ext.cog_slash(name='ping', guild_ids=guild_ids)
    async def ping(self, ctx):
        await ctx.send("pong!")

    @cog_ext.cog_slash(name='createdataset', guild_ids=guild_ids)
    async def createdataset(self, ctx, name:str):
        author = ctx.author
        if dbfunc.get_num_datasets(author.id) >= plotvars.max_datasets:
            description=f"You have reached your maximum of `{plotvars.max_datasets}` datasets. You can delete your existing datasets using `/removedataset <dataset_name>`"
            await ctx.send(embed=utils.error_embed(description))
            return
        try:
            dbfunc.set_dataset(author.id, name)

            title=f"Dataset `{name}` has been created!"
            description=""
            color=discord.Color.green()
            await ctx.send(embed=utils.create_embed(title, description, color))
        except:
            description="You already have a dataset with the same name!"
            await ctx.send(embed=utils.error_embed(description))
            return

    @cog_ext.cog_slash(name='removedataset', guild_ids=guild_ids)
    async def removedataset(self, ctx, name:str):
        author = ctx.author
        num_removed = dbfunc.remove_dataset(author.id, name)
        if num_removed == 0:
            description="There is no dataset with this name to remove!"
            await ctx.send(embed=utils.error_embed(description))
        else:
            title=f"Dataset `{name}` successfully removed!"
            description=""
            color=discord.Color.green()
            await ctx.send(embed=utils.create_embed(title, description, color))
    
    @cog_ext.cog_slash(name='addnumberrow', guild_ids=guild_ids)
    async def addnumberrow(self, ctx, dataset_name:str, row_name:str, numbers:str, separator:str=" "):

        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name, check_length=True)
        if datadict is None:
            return

        #turn numbers string into list of numbers
        numlist = None
        try:
            numlist = utils.str2numlist(numbers, separator)
        except Exception as e:
            description="Either one of your values is not a number, or your list is not properly formatted. Please try again, or use `/help addnumberrow` for assistance."
            await ctx.send(embed=utils.error_embed(description))
            return

        #Add the numbers to the end of a pre-existing list or just use the values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = numlist
        else:
            new_row_values = previous_row_values.copy()
            for num in numlist:
                new_row_values.append(num)
            datadict[row_name] = new_row_values
        
        #Write the data to the database
        data_written = await asyncutils.log_data_to_database(ctx, dataset_name, datadict)
        if data_written == False:
            return
        
        title=f"Number values have been added to the `{row_name}` row!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))


    @cog_ext.cog_slash(name='addstringrow', guild_ids=guild_ids)
    async def addstringrow(self, ctx, dataset_name:str, row_name:str, strings:str, separator:str=" "):

        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name, check_length=True)
        if datadict is None:
            return

        #turn strings into list of strings
        strlist = None
        try:
            strlist = utils.str2strlist(strings, separator)
        except:
            description="Your list is not properly formatted. Please try again, or use `/help addstringrow` for assistance."
            await ctx.send(embed=utils.error_embed(description))
            return

        #Add the strings to the end of a pre-existing list or just use the values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = strlist
        else:
            new_row_values = previous_row_values.copy()
            for string in strlist:
                new_row_values.append(string)
            datadict[row_name] = new_row_values
        
        #Write the data to the database
        data_written = await asyncutils.log_data_to_database(ctx, dataset_name, datadict)
        if data_written == False:
            return
        
        title=f"String values have been added to the `{row_name}` row!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))

    @cog_ext.cog_slash(name='addrandomnumrow', guild_ids=guild_ids)
    async def addrandomnumberrow(self, ctx, dataset_name:str, row_name:str, amount_of_random_numbers:int, minimum_number:float, maximum_number:float):
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name, check_length=True)
        if datadict is None:
            return

        #Get the random list of numbers
        numlist = None
        try:
            numlist=utils.random_num_list(amount_of_random_numbers, minimum_number, maximum_number)
        except:
            description=f"An error occured while generating the random numbers. Make sure that your minimum and maximum values were entered as numbers and try again."
            await ctx.send(embed=utils.error_embed(description))
            return


        #Add the values to the end of a pre-existing list or just use the values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = numlist
        else:
            new_row_values = previous_row_values.copy()
            for num in numlist:
                new_row_values.append(num)
            datadict[row_name] = new_row_values

        #Write the data to the database
        data_written = await asyncutils.log_data_to_database(ctx, dataset_name, datadict)
        if data_written == False:
            return
        
        title=f"`{amount_of_random_numbers}` random number values of range `{minimum_number}` to `{maximum_number}` have been added to the `{row_name}` row! To view the values use `/viewdata `{dataset_name}`"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))

    @cog_ext.cog_slash(name='viewdata', guild_ids=guild_ids)
    async def viewdata(self, ctx, dataset_name:str):
        author = ctx.author
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
        if datadict is None:
            return

        title=f"Data in the dataset `{dataset_name}`:"
        description = ""
        color=discord.Color.orange()
        for key, value in datadict.items():
            description+=f"{key}: {value} \n"
        description+=f"Plot Title: {dbfunc.get_plot_title(author.id, dataset_name)}\n"
        description+=f"Axis info: {dbfunc.get_axis_info(author.id,dataset_name)}\n"

        try:   
            await ctx.send(embed=utils.create_embed(title=title, description=description, color=color))
        except:
            msg = f"Your data was unable to be sent, most likely due to discord's message character limit. Use `/viewdataintxt` to get the data with no character limit."
            await ctx.send(embed=utils.error_embed(msg))

    @cog_ext.cog_slash(name='viewdataintxt', guild_ids=guild_ids)
    async def viewdataintxt(self, ctx, dataset_name:str):
        author = ctx.author
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
        if datadict is None:
            return
        strtowrite=f"Data in the dataset `{dataset_name}`:\n"
        for key, value in datadict.items():
            strtowrite+=f"{key}: {value} \n"
        strtowrite+=f"Plot Title: {dbfunc.get_plot_title(author.id, dataset_name)}\n"
        strtowrite+=f"Axis info: {dbfunc.get_axis_info(author.id,dataset_name)}\n"

        txtfile = f"{author.name}_{dataset_name}.txt"

        file = open(txtfile, "w+")
        file.write(strtowrite)
        file.close()

        await ctx.send(file=discord.File(txtfile))

        os.remove(txtfile)

    @cog_ext.cog_slash(name='viewgraphdata', guild_ids=guild_ids)
    async def viewgraphdata(self, ctx, dataset_name:str):
        #Get the graph data
        graph_data_dict = await asyncutils.get_graph_data_dictionary(ctx, dataset_name)
        if graph_data_dict is None:
            return
        
        title=f"Saved graph data in the dataset `{dataset_name}`:"
        description = ""
        color=discord.Color.orange()
        for key, value in graph_data_dict.items():
            description+=f"{key}: {value} \n"
        
        try:   
            await ctx.send(embed=utils.create_embed(title=title, description=description, color=color))
        except:
            msg = f"Your data was unable to be sent, most likely due to discord's message character limit. Use `/viewdataintxt` to get the data with no character limit."
            await ctx.send(embed=utils.error_embed(msg))

    @cog_ext.cog_slash(name='viewgraphdataintxt', guild_ids=guild_ids)
    async def viewgraphdataintxt(self, ctx, dataset_name:str):
        author = ctx.author
        #Get the data
        graph_data_dict = await asyncutils.get_graph_data_dictionary(ctx, dataset_name)
        if graph_data_dict is None:
            return

        strtowrite=f"Saved graph data in the dataset `{dataset_name}`:\n"
        for key, value in graph_data_dict.items():
            strtowrite+=f"{key}: {value} \n"

        txtfile = f"{author.name}_{dataset_name}_graph.txt"

        file = open(txtfile, "w+")
        file.write(strtowrite)
        file.close()

        await ctx.send(file=discord.File(txtfile))

        os.remove(txtfile)

    @cog_ext.cog_slash(name='viewdatasets', guild_ids=guild_ids)
    async def viewdatasets(self, ctx):
        author = ctx.author
        title=f'{author.name}\'s datasets:'
        description = dbfunc.get_names_of_datasets(author.id)
        color=discord.Color.orange()
        await ctx.send(embed=utils.create_embed(title=title, description=description, color=color))

    @cog_ext.cog_slash(name='removerow', guild_ids=guild_ids)
    async def removerow(self, ctx, dataset_name:str, row_name:str):
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
        if datadict is None:
            return
        
        values = datadict.get(row_name, None)
        if values is None:
            description=f"Your row name doesn't exist in dataset `{dataset_name}`. Please double-check the names using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return

        del datadict[row_name]

        #Write the data to the database
        data_written = await asyncutils.log_data_to_database(ctx, dataset_name, datadict)
        if data_written == False:
            return
        
        title=f"Row `{row_name}` has been deleted from dataset `{dataset_name}`!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))

    
    @cog_ext.cog_slash(name='addcolorrow', guild_ids=guild_ids)
    async def addcolorrow(self, ctx, dataset_name:str, row_name:str, colors:str, separator:str=" "):
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name, check_length=True)
        if datadict is None:
            return

        #turn colors string into list of colors
        colorlist = None
        try:
            colorlist = utils.str2colorlist(colors, separator)
        except:
            description="Either one of your values is not a color, or your list is not properly formatted. Please try again or use `/help addcolorrow` for assistance."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        #Add the colors to the end of a pre-existing list or just use the values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = colorlist
        else:
            new_row_values = previous_row_values.copy()
            for color in colorlist:
                new_row_values.append(color)
            datadict[row_name] = new_row_values

        #Write the data to the database
        data_written = await asyncutils.log_data_to_database(ctx, dataset_name, datadict)
        if data_written == False:
            return

        title=f"Color values have been added to the `{row_name}` row!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))


    @cog_ext.cog_slash(name='addrandomcolorrow', guild_ids=guild_ids)
    async def addrandomcolorrow(self, ctx, dataset_name:str, row_name:str, amount_of_random_colors:int):
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name, check_length=True)
        if datadict is None:
            return
    
        #Create random list of colors
        colorlist=[]
        try:
            for _ in range(amount_of_random_colors):
                colorlist.append(utils.generate_random_color())
        except:
            description=f"An error with color generation occurred on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(description))
            return
        
        #Add the colors to the end of a pre-existing list or just use the values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = colorlist
        else:
            new_row_values = previous_row_values.copy()
            for color in colorlist:
                new_row_values.append(color)
            datadict[row_name] = new_row_values

        #Write the data to the database
        data_written = await asyncutils.log_data_to_database(ctx, dataset_name, datadict)
        if data_written == False:
            return


        title=f"`{amount_of_random_colors}` color values have been added to the `{row_name}` row!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))

def setup(bot):
    bot.add_cog(DataSetCommands(bot))