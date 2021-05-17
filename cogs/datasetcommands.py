import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import db.plotdbfunctions as dbfunc
import utils
import plotvars
from plotvars import guild_ids

class DataSetCommands(commands.Cog):
    @cog_ext.cog_slash(name='ping', guild_ids=guild_ids)
    async def ping(self, ctx):
        await ctx.send("pong!")

    @cog_ext.cog_slash(name='createdataset', guild_ids=guild_ids)
    async def createdataset(self, ctx, name:str):
        author = ctx.author
        if dbfunc.get_num_datasets(author.id) >= plotvars.max_datasets:
            await ctx.send(f"You have reached your maximum of {plotvars.max_datasets} datasets. You can delete your existing datasets using `/removedataset <dataset_name>`")
            return
        try:
            dbfunc.set_dataset(author.id, name)

            title=f"Dataset `{name}` has been created!"
            description=""
            color=discord.Color.green()
            await ctx.send(embed=utils.create_embed(title, description, color))
        except:
            await ctx.send("You already have a dataset with the same name!")

    @cog_ext.cog_slash(name='removedataset', guild_ids=guild_ids)
    async def removedataset(self, ctx, name:str):
        author = ctx.author
        num_removed = dbfunc.remove_dataset(author.id, name)
        if num_removed == 0:
            await ctx.send("There is no dataset with this name to remove!")
        else:
            title=f"Dataset `{name}` successfully removed!"
            description=""
            color=discord.Color.green()
            await ctx.send(embed=utils.create_embed(title, description, color))
    
    @cog_ext.cog_slash(name='addnumrow', guild_ids=guild_ids)
    async def addnumrow(self, ctx, dataset_name:str, row_name:str, values:str):
        author = ctx.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, dataset_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{dataset_name}`!")
            return

        #turn string into list of numbers
        numlist = None
        try:
            numlist = utils.str2numlist(values)
        except Exception as e:
            await ctx.send(f"{str(e)}")
            await ctx.send("Either one of your values is not a number, or your list is not properly formatted. Please try again, or use `/help addnumrow` for assistance.")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
            return

        #Add the values to the end of a pre-existing list or just use the x values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = numlist
        else:
            new_row_values = previous_row_values.copy()
            for num in numlist:
                new_row_values.append(num)
            datadict[row_name] = new_row_values
        
        #add the new data to the database
        dict2str = str(datadict)
        try:
            dbfunc.set_dataset_data(author.id, dataset_name, dict2str)
        except:
            await ctx.send(f"You don't have a dataset with the name `{dataset_name}` to add the data to!")
            return
        
        title=f"Number values have been added to the {row_name} row!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))


    @cog_ext.cog_slash(name='addstringrow', guild_ids=guild_ids)
    async def addstringrow(self, ctx, dataset_name:str, row_name:str, values:str):
        author = ctx.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, dataset_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{dataset_name}`!")
            return

        #turn string into list of numbers
        numlist = None
        try:
            numlist = utils.str2strlist(values)
        except:
            await ctx.send("Your list is not properly formatted. Please try again, or use `/help addstringrow` for assistance.")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
            return

        #Add the values to the end of a pre-existing list or just use the x values
        previous_row_values = datadict.get(row_name, None)
        if previous_row_values is None:
            datadict[row_name] = numlist
        else:
            new_row_values = previous_row_values.copy()
            for num in numlist:
                new_row_values.append(num)
            datadict[row_name] = new_row_values
        
        #add the new data to the database
        dict2str = str(datadict)
        try:
            dbfunc.set_dataset_data(author.id, dataset_name, dict2str)
        except:
            await ctx.send(f"You don't have a dataset with the name `{dataset_name}` to add the data to!")
            return
        
        title=f"String values have been added to the {row_name} row!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))

    @cog_ext.cog_slash(name='viewdata', guild_ids=guild_ids)
    async def viewdata(self, ctx, dataset_name:str):
        author = ctx.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, dataset_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{dataset_name}`!")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
            return

        title=f"Data in the dataset {dataset_name}:"
        description = ""
        color=discord.Color.orange()
        for key, value in datadict.items():
            description+=f"{key}: {value} \n"

        await ctx.send(embed=utils.create_embed(title=title, description=description, color=color))

    @cog_ext.cog_slash(name='viewdatasets', guild_ids=guild_ids)
    async def viewdatasets(self, ctx):
        author = ctx.author
        title=f'{author.name}\'s datasets:'
        description = dbfunc.get_names_of_datasets(author.id)
        color=discord.Color.orange()
        await ctx.send(embed=utils.create_embed(title=title, description=description, color=color))

    @cog_ext.cog_slash(name='removerow', guild_ids=guild_ids)
    async def removerow(self, ctx, dataset_name:str, row_name:str):
        author = ctx.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, dataset_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{dataset_name}`!")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
            return
        
        values = datadict.get(row_name, None)
        if values is None:
            await ctx.send(f"Your row name doesn't exist in dataset {dataset_name}. Please double-check the names using `/viewdata <dataset_name>` and try again.")
            return

        del datadict[row_name]

        dbfunc.set_dataset_data(author.id, dataset_name, str(datadict))
        
        title=f"Row {row_name} has been deleted from dataset {dataset_name}!"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))


def setup(bot):
    bot.add_cog(DataSetCommands(bot))