import discord
from discord.ext import commands
import db.plotdbfunctions as dbfunc
from discord_slash import cog_ext, SlashContext
import utils
import plotvars
from plotvars import guild_ids
import numpy
import matplotlib.pyplot as plt
import os


class PlotGenerationCommands(commands.Cog):
    
    @cog_ext.cog_slash(name='scatterplot', guild_ids=guild_ids, description="Create a scatterplot")
    async def scatterplot(self, ctx, dataset_name, x_row:str, y_row:str, x_label:str="", y_label:str="", size_row:str=""):
        author = ctx.author
        #Recieve data in string format from db
        datastr = None
        try:
            datastr= dbfunc.get_dataset_data(author.id, dataset_name)
        except:
            description=f"You don't have a dataset with the name `{dataset_name}`!"
            await ctx.send(embed=utils.error_embed(description))
            return

        #Turn data in string format to dict format (this should only fail if the bot did something wrong)
        datadict = None
        try:
            datadict=utils.str2dict(datastr)
        except:
            description=f"An error happened with the dictionary formatting on our end. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(description))
            return

        # Check if the x, y and size rows exist in the dataset
        x_values = datadict.get(x_row, None)
        y_values = datadict.get(y_row, None)
        size_values = datadict.get(size_row, None) if size_row != "" else ""
        if x_values is None:
            description=f"Your row name for the \"x\" values doesn't exist in dataset {dataset_name}. Please double-check the names using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        if y_values is None:
            description=f"Your row name for the \"y\" values doesn't exist in dataset {dataset_name}. Please double-check the names using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        if size_values is None:
            description=f"Your row name for the \"size\" values doesn't exist in dataset {dataset_name}. Please double-check the names using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        #Check if the x, y and size rows are number lists and are the same length
        verify_x = utils.verify_list_is_numlist(x_values)
        if verify_x is None:
            description="Your row of \"x\" values are not all numbers. Please double-check the values using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        verify_y = utils.verify_list_is_numlist(y_values)
        if verify_y is None:
            description="Your row of \"y\" values are not all numbers. Please double-check the values using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        verify_sizes= utils.verify_list_is_numlist(size_values) if size_values != "" else ""
        if verify_sizes is None:
            description="Your row of \"size\" values are not all numbers. Please double-check the values using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return

        size_length = len(size_values) if size_values != "" else len(x_values)
        if len(x_values) != len(y_values) or len(x_values) != size_length:
            description="Your rows of \"x\", \"y\" and \"size\" values do not have the same length, which is required for a scatterplot. Please double-check the values using `/viewdata <dataset_name>` and try again."
            await ctx.send(embed=utils.error_embed(description))

        #Make the graph
        x_npy = numpy.array(x_values)
        y_npy = numpy.array(y_values)
        size_npy = numpy.array(size_values) if size_values != "" else None
        plt.scatter(x_npy, y_npy, s=size_npy)
        potential_title=dbfunc.get_plot_title(author.id, dataset_name)
        plt.title(dataset_name if potential_title is None else potential_title)
        plt.xlabel(x_row if x_label == "" else x_label)
        plt.ylabel(y_row if y_label == "" else y_label)

        
        file_name = f'plot_{dataset_name}.png'
        
        plt.savefig(file_name, dpi='figure')
        plt.close()
        
        channel = ctx.channel
        await channel.send(file=discord.File(file_name))
        os.remove(file_name)
        

def setup(bot):
    bot.add_cog(PlotGenerationCommands(bot))