import discord
from discord.ext import commands
import db.plotdbfunctions as dbfunc
import utils
import plotvars

class DataSetCommands(commands.Cog):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command()
    async def createdataset(self, ctx, name:str):
        author = ctx.message.author
        if dbfunc.get_num_datasets(author.id) >= plotvars.max_datasets:
            await ctx.send(f"You have reached your maximum of {plotvars.max_datasets} datasets. You can delete your existing datasets using `.removedataset <dataset_name>`")
            return
        try:
            dbfunc.set_dataset(author.id, name)
            await ctx.send(f"Dataset `{name}` has been created! To add rows, use `.addnumrow <dataset_name> <row_name> <values>` and `.addstringrow <dataset_name> <row_name> <values>`.")
        except:
            await ctx.send("You already have a dataset with the same name!")

    @commands.command()
    async def removedataset(self, ctx, name:str):
        author = ctx.message.author
        num_removed = dbfunc.remove_dataset(author.id, name)
        if num_removed == 0:
            await ctx.send("There is no dataset with this name to remove!")
        else:
            await ctx.send(f"Dataset `{name}` successfully removed!")
    
    @commands.command()
    async def addnumrow(self, ctx, ds_name:str, row_name:str, * values):
        valuesstr = ' '.join(values)
        author = ctx.message.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, ds_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{ds_name}`!")
            return

        #turn string into list of numbers
        numlist = None
        try:
            numlist = utils.str2numlist(valuesstr)
        except Exception as e:
            await ctx.send(f"{str(e)}")
            await ctx.send("Either one of your values is not a number, or your list is not properly formatted. Please try again, or use `.help addnumrow` for assistance.")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `.report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
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
            dbfunc.set_dataset_data(author.id, ds_name, dict2str)
        except:
            await ctx.send(f"You don't have a dataset with the name `{ds_name}` to add the data to!")
            return
        
        await ctx.send(f"Number values have been added to the {row_name} row!")


    @commands.command()
    async def addstringrow(self, ctx, ds_name:str, row_name:str, * values):
        valuesstr = ' '.join(values)
        author = ctx.message.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, ds_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{ds_name}`!")
            return

        #turn string into list of numbers
        numlist = None
        try:
            numlist = utils.str2strlist(valuesstr)
        except:
            await ctx.send("Your list is not properly formatted. Please try again, or use `.help addstringrow` for assistance.")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `.report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
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
            dbfunc.set_dataset_data(author.id, ds_name, dict2str)
        except:
            await ctx.send(f"You don't have a dataset with the name `{ds_name}` to add the data to!")
            return
        
        await ctx.send(f"String values have been added to the {row_name} row!")

    @commands.command()
    async def viewdata(self, ctx, ds_name:str):
        author = ctx.message.author
        datastr = None
        #Recieve data in string format from db
        try:
            datastr= dbfunc.get_dataset_data(author.id, ds_name)
        except:
            await ctx.send(f"You don't have a dataset with the name `{ds_name}`!")
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            await ctx.send(f"An error happened with the dictionary formatting on our end. Please use `.report` to report the issue or get help in our support server: {plotvars.support_discord_link}")
            return

        result_str = ""
        for key, value in datadict.items():
            result_str+=f"{key}: {value} \n"

        await ctx.send(result_str)

    @commands.command()
    async def viewdatasets(self, ctx):
        author = ctx.message.author
        await ctx.send(dbfunc.get_names_of_datasets(author.id))

        
        

        
    


def setup(bot):
    bot.add_cog(DataSetCommands(bot))