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


class Scatterplot(commands.Cog):
    
    @cog_ext.cog_slash(name='scatterplot', guild_ids=guild_ids, description="Generates a scatterplot!")
    async def scatterplot(self, ctx, dataset_name, x_row:str, y_row:str, x_label:str="", y_label:str="", size_row:str="", color_row_or_one_color:str="", transparency:float=1, saveas:str=""):
        #Creates a scatterplot by calling the _scatterplot method
        await self._scatterplot(ctx, dataset_name, x_row, y_row, x_label, y_label, size_row, color_row_or_one_color, transparency, saveas)

    async def _scatterplot(self, ctx, dataset_name, x_row:str, y_row:str, x_label:str="", y_label:str="", size_row:str="", color_row_or_one_color:str="", transparency:float=1, saveas:str=""):
        """Generates a scatterplot with the given arguments.
            This method also sanitizes all inputs so the matplotlib generation does not fail.

            Sanitation that is done:
            - Makes sure that X, Y and size rows are rows of numbers
            - Makes sure that the colors input is a row of colors or just one color (if applicable)
            - Makes sure that all applicable rows have the same length
            - Makes sure that the transparency of the dots is in between 0 and 1

        Args:
            dataset_name ([type]): Name of the dataset
            x_row (str): Name of a row in the dataset that will correspond to the X values in the scatterplot
            y_row (str): Name of a row in the dataset that will correspond to the Y values in the scatterplot
            x_label (str, optional): The label given to the X values. Defaults to "", and will just use the name of the X row if empty.
            y_label (str, optional): The label given to the Y values. Defaults to "", and will just use the name of the Y row if empty.
            size_row (str, optional): Name of a row in the dataset that will correspond to the sizes of the dots in the scatterplot. Defaults to "", where all the sizes will be default.
            color_row_or_one_color (str, optional): EITHER the name of a row in the dataset that corresponds to the colors of the dots, or one color for all of the dots to be. Defaults to "", where a matplotlib default color will be used.
            transparency (float, optional): How transparent the dots in the scatterplot are. Defaults to 1.
            saveas (str, optional): Name to save the graph as in the dataset. Defaults to "", in which the graph will not be saved.
        """
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
                if color_row_or_one_color != "": 
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
        
        
        #Turn all of the values into numpy arrays (if applicable)
        x_npy = numpy.array(x_values)
        y_npy = numpy.array(y_values)
        size_npy = numpy.array(size_values) if size_values != "" else None
        colors_npy = numpy.array(color_values) if color_is_row else color_values
        colors_npy = None if color_row_or_one_color == "" else colors_npy

        #Create the matplotlib graph
        plt.figure()
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
        description=f"Plot has been saved as {saveas}! Use `/viewgraphdata {dataset_name}` to view the graph data and `/plotgenerate {saveas}` to generate the plot again." if saveas != "" else ""
        plot_embed = utils.create_embed(f"Scatterplot for {author.name}", description, discord.Color.dark_orange())
        plot_embed.set_image(url=f"attachment://{file_name}")
        await ctx.send(embed=plot_embed, file=file)
        os.remove(file_name)


        if saveas != "":
            graph_data = {
                "name": "scatterplot",
                "x_row": x_row,
                "y_row": y_row,
                "x_label": x_label,
                "y_label": y_label,
                "size_row": size_row,
                "color_row_or_one_color": color_row_or_one_color,
                "transparency": transparency
            }

            await self._save_graph_data(ctx, dataset_name, graph_data)


    
    async def _save_graph_data(ctx, dataset_name:str, saveas:str,  graph_data):
        #Get the pre-existing graph data
        graph_data_dict = await asyncutils.get_graph_data_dictionary(ctx, dataset_name)
        if graph_data_dict is None:
            return
        
        #Set the dictionary value for the saveas to be the graph data
        graph_data_dict[saveas] = graph_data

        #Write the graph data to the database
        graph_data_written = await asyncutils.log_graph_data_to_database(ctx, dataset_name, graph_data_dict)
        if graph_data_written == False:
            return
        

def setup(bot):
    bot.add_cog(Scatterplot(bot))