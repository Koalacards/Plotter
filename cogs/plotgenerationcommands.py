import discord
from discord.ext import commands
import db.plotdbfunctions as dbfunc
from discord_slash import cog_ext
import utils
from plotvars import guild_ids
import numpy
import matplotlib.pyplot as plt
import os
import asyncutils


class PlotGenerationCommands(commands.Cog):
    
    @cog_ext.cog_slash(name='scatterplot', guild_ids=guild_ids, description="Create a scatterplot")
    async def scatterplot(self, ctx, dataset_name, x_row:str, y_row:str, x_label:str="", y_label:str="", size_row:str=""):
        author = ctx.author

        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
        if datadict is None:
            return

        # Check if the x, y and size rows exist in the dataset and are number lists
        rows_to_check = [x_row, y_row]
        if size_row != "":
            rows_to_check.append(size_row)
        
        row_values = await asyncutils.verify_rows_are_rows_of_numbers(ctx, dataset_name, datadict, rows_to_check)
        if row_values is None:
            return

        x_values = row_values[0]
        y_values = row_values[1]
        size_values = row_values[2] if size_row != "" else ""

        size_length = len(size_values) if size_values != "" else len(x_values)
        if len(x_values) != len(y_values) or len(x_values) != size_length:
            description=f"Your rows of \"x\", \"y\" and \"size\" values do not have the same length, which is required for a scatterplot. Please double-check the values using `/viewdata {dataset_name}` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        
        #Make the graph
        x_npy = numpy.array(x_values)
        y_npy = numpy.array(y_values)
        size_npy = numpy.array(size_values) if size_values != "" else None
        plt.scatter(x_npy, y_npy, s=size_npy)
        potential_title=dbfunc.get_plot_title(author.id, dataset_name)
        plt.title(potential_title)
        plt.axis(utils.sanitize_axis_info(author, dataset_name))
        plt.xlabel(x_row if x_label == "" else x_label)
        plt.ylabel(y_row if y_label == "" else y_label)

        
        file_name = f'plot_{dataset_name}.png'
        
        plt.savefig(file_name, dpi='figure')
        plt.close()
        
        file=discord.File(file_name)
        plot_embed = utils.create_embed(f"Scatterplot for {author.name}", "", discord.Color.dark_orange())
        plot_embed.set_image(url=f"attachment://{file_name}")
        await ctx.send(embed=plot_embed, file=file)
        os.remove(file_name)
        
        

def setup(bot):
    bot.add_cog(PlotGenerationCommands(bot))