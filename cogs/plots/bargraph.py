import discord
from discord.ext import commands
from discord_slash import cog_ext
import utils
import plotvars
from plotvars import guild_ids
import numpy as np
import matplotlib.pyplot as plt
import os
import asyncutils
import cogs.plots.plothelpers as plothelpers

class BarGraph(commands.Cog):

    @cog_ext.cog_slash(name='bargraph', guild_ids=guild_ids, description="Generates a bar graph!")
    async def bargraph(self, ctx, dataset_name:str, x_row:str, height_row:str, x_label:str="", y_label:str="", width:float=0.8, bottom_coords_row:str="", align:str="center", color_row_or_one_color:str="", saveas:str=""):
        #Calls the _bargraph method
        await self._bargraph(ctx, dataset_name, x_row, height_row, x_label, y_label, width, bottom_coords_row, align, color_row_or_one_color, saveas)

    async def _bargraph(self, ctx, dataset_name:str, x_row:str, height_row:str, x_label:str="", y_label:str="", width:float=0.8, bottom_coords_row:str="", align:str="center", color_row_or_one_color:str="", saveas:str="",
        save_and_close:bool=True, create_figure:bool=True, set_common_plot_info:bool=True, send_message:bool=True):
        """Generates a Bar Graph with the given arguments.
            This method also sanitizes all necessary outputs so that the matplotlib does not fail.

            Sanitation that is done:
            - Make sure that X, Height, and Bottom rows are rows of numbers
            - Makes sure that the colors input is a row of colors or just one color (if applicable)
            - Makes sure that all applicable rows (number or color) have the same length
            - Makes sure that the width is a float
            - Makes sure that align is either "center" or "edge"


        Args:
            dataset_name (str): Name of the dataset
            x_row (str): Name of the number row corresponding to x coordinates of the bars
            height_row (str): Name of the number row corresponding to the heights of the bars
            x_label (str, optional): The label given to the X values. Defaults to "".
            y_label (str, optional): The label given to the Y values.  Defaults to "".
            width (float, optional): The width of the bars in the bar graph, as a float. Defaults to 0.8.
            bottom_coords_row (str, optional): The label given to the row corresponding to the bottom heights of the bars. Defaults to "", where all of the bars will start at y=0.
            align (str, optional): The bar graph alignment with regard to the x value. Is either "center" or "edge.
            color_row_or_one_color (str, optional): EITHER the name of a row in the dataset that corresponds to the colors of the dots, or one color for all of the dots to be. Defaults to "", where a matplotlib default color will be used.
            saveas (str, optional): Name to save the graph as in the dataset. Defaults to "", in which the graph will not be saved.
            save_and_close(bool, optional): Whether or not to save the figure and clear data(used in combination graphs)
            create_figure(bool, optional): Whether or not to create a new matplotlib figure(used in combination graphs)
            set_common_plot_info(bool, optional): Whether or not to set the common plot info for a figure(used in combination graphs)
            send_message(bool, optional): Whether or not to send the message with the plot in it (used in combination graphs)
        """

        author = ctx.author

        #Sanitize the inputs
        answer_dict = await _sanitize_bargraph_inputs(ctx, dataset_name, x_row, height_row, bottom_coords_row, width, align, color_row_or_one_color)
        if answer_dict is None:
            return
        
        values_exist = utils.check_values_exist_for_keys(answer_dict, ["x", "height", "bottom", "width", "align", "color"])
        if values_exist == False:
            error_msg = f"An error occured on our end when generating the bar graph: Answer dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return

        x = answer_dict["x"]
        height = answer_dict["height"]
        bottom = answer_dict["bottom"]
        width_sanitized = answer_dict["width"]
        align_sanitized = answer_dict["align"]
        color = answer_dict["color"]

        #Create the matplotlib graph
        if create_figure:
            plothelpers.create_figure()

        if set_common_plot_info:
            await plothelpers.set_common_plot_info(ctx, dataset_name, x_label, y_label)

        create_bar_graph(x, height, bottom, width_sanitized, align_sanitized, color)

        file_name = f'plot_{dataset_name}.png'

        if save_and_close:
            plothelpers.save_and_close(file_name)

        if save_and_close and send_message:
            file=discord.File(file_name)
            description=f"Plot has been saved as {saveas}! Use `/viewgraphdata {dataset_name}` to view the graph data and `/plotgenerate {dataset_name} {saveas}` to generate the plot again." if saveas != "" else ""
            plot_embed = utils.create_embed(f"Bar Graph for {author.name}", description, discord.Color.dark_orange())
            plot_embed.set_image(url=f"attachment://{file_name}")
            await ctx.send(embed=plot_embed, file=file)
            os.remove(file_name)

        if saveas != "":
            graph_data = {
                "name": "bargraph",
                "x_row": x_row,
                "height_row": height_row,
                "x_label": x_label,
                "y_label": y_label,
                "width": width,
                "bottom_coords_row": bottom_coords_row,
                "align": align,
                "color_row_or_one_color": color_row_or_one_color
            }

            await asyncutils.save_graph_data(ctx, dataset_name, saveas, graph_data)
        


async def _sanitize_bargraph_inputs(ctx, dataset_name:str, x_row:str, height_row:str, bottom_coords_row:str, width:float, align:str, color_row_or_one_color:str):
    #Get the data
    datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
    if datadict is None:
        return None

    #Check if the x_row, height_row and bottom_coords_row (if exists) are number lists
    rows_to_check = [x_row, height_row]
    if bottom_coords_row != "":
        rows_to_check.append(bottom_coords_row)

    row_values = await asyncutils.verify_rows_are_rows_of_numbers(ctx, dataset_name, datadict, rows_to_check)
    if row_values is None:
        return None

    x_values = row_values[0]
    height_values = row_values[1]
    bottom_values = row_values[2] if bottom_coords_row != "" else ""

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
                return None
    else:
        color_values = check_color_row[0]

    #If the color input is a row of colors, make sure the row is a row of colors
    if color_is_row:
        try:
            utils.verify_list_is_colorlist(color_values)
        except:
            description=f"The row you entered for colors was not a full list of hexcode colors. Please double-check the colors using `/viewdata {dataset_name}` and try again."
            await ctx.send(embed=utils.error_embed(description))
            return None
    
    #Check that the sizes of all rows are the same
    bottom_length = len(bottom_values) if bottom_values != "" else len(x_values)
    color_length = len(color_values) if color_is_row else len(x_values)
    if len(x_values) != len(height_values) or len(x_values) != bottom_length or len(x_values) != color_length:
        description=f"Your rows of \"x\", \"height\", \"bottom\" and \"color\" values do not have the same length, which is required for a bar graph. Please double-check the values using `/viewdata {dataset_name}` and try again."
        await ctx.send(embed=utils.error_embed(description))
        return None

    #Check that width is a float
    try:
        width = float(width)
    except:
        description=f"Your width input must be a number. Please change the input and try again."
        await ctx.send(embed=utils.error_embed(description))
        return None

    #Check that align is either "center" or "edge"
    if align != "center" and align != "edge":
        description=f"Your input value for align is not either `center` or `edge`. Please change the input and try again."
        await ctx.send(embed=utils.error_embed(description))
        return None
    
    #Turn all the lists into numpy arrays
    x_npy = np.array(x_values)
    height_npy = np.array(height_values)
    bottom_npy = np.array(bottom_values) if bottom_values != "" else None
    colors_npy = np.array(color_values) if color_is_row else color_values
    colors_npy = None if color_row_or_one_color == "" else colors_npy

    answer_dict = {
        "x": x_npy,
        "height": height_npy,
        "bottom": bottom_npy,
        "width": width,
        "align": align,
        "color": colors_npy
    }

    return answer_dict

#Creates the bar graph with the given inputs
def create_bar_graph(x, height, bottom, width, align, color) -> None:
    plt.bar(x, height, width=width, bottom=bottom, align=align, color=color)


def setup(bot):
    bot.add_cog(BarGraph(bot))