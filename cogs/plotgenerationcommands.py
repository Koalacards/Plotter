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
    async def scatterplot(self, ctx, dataset_name, x_row:str, y_row:str, x_label:str="", y_label:str="", size_row:str="", color_row_or_one_color:str="", transparency:float=1):
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

        #Check if the color row exists in the dataset or is an individual color
        check_color_row=await asyncutils.verify_rows_exist_in_dataset(ctx, dataset_name, datadict, [color_row_or_one_color], send_error_message=False)
        color_is_row=True
        color_values = None
        if check_color_row is None:
            color_is_row=False
            try:
                utils.verify_string_is_color(color_row_or_one_color)
                color_values = color_row_or_one_color
            except:
                description=f"Your color input was neither the name of a row in the database nor a single color. Please check the input and try again."
                await ctx.send(embed=utils.error_embed(description))
                return
        else:
            color_values = check_color_row[0]

        #If the color input is a row of colors, make sure the row is a row of colors
        if color_is_row:
            try:
                utils.verify_list_is_colorlist(color_values)
            except:
                description=f"The row you entered for colors was not a full list of hexcode colors. Please double-check the colors using `/viewdata {dataset_name}` and try again."
                await ctx.send(embed=utils.error_embed(description))
                return
        
        #Check that the sizes of all rows are the same
        size_length = len(size_values) if size_values != "" else len(x_values)
        color_length = len(color_values) if color_is_row else len(x_values)
        if len(x_values) != len(y_values) or len(x_values) != size_length or len(x_values) != color_length:
            description=f"Your rows of \"x\", \"y\", \"size\" and \"color\" values do not have the same length, which is required for a scatterplot. Please double-check the values using `/viewdata {dataset_name}` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return

        #Check that transparency is a float and between 0 and 1
        try:
            transparency = float(transparency)
            if transparency < 0 or transparency > 1:
                raise Exception()
        except:
            description=f"Your transparency input must be a number between 0 and 1. Please change the input and try again."
            await ctx.send(embed=utils.error_embed(description))
            return
        
        
        #Make the graph
        x_npy = numpy.array(x_values)
        y_npy = numpy.array(y_values)
        size_npy = numpy.array(size_values) if size_values != "" else None
        colors_npy = numpy.array(color_values) if color_is_row else color_values
        colors_npy = None if color_row_or_one_color == "" else colors_npy
        plt.scatter(x_npy, y_npy, s=size_npy, c=colors_npy, alpha=transparency)
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