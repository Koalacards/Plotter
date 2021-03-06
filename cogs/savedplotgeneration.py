import discord
from discord.ext import commands
from discord_slash import cog_ext
from matplotlib.pyplot import bar
import utils
import plotvars
from plotvars import guild_ids
import asyncutils
from cogs.plots.scatterplot import Scatterplot
from cogs.plots.bargraph import BarGraph
import os
import cogs.plots.plothelpers as plothelpers
import cogs.options as options

class SavedPlotGeneration(commands.Cog):

    @cog_ext.cog_slash(name='plotgenerate', guild_ids=guild_ids, description="Generates a saved plot from one of yoru datasets!", options=options.plotgenerate_options)
    async def plotgenerate(self, ctx, dataset_name:str, saved_plot_name:str):
        """Generates a saved plot from a dataset.

        This method will essentially run the graph command without the user having to input a ton of information

        Args:
            dataset_name (str): name of the dataset
            saved_plot_name (str): Name of the saved plot a user generated earlier
        """

        await self._plotgenerate(ctx, dataset_name, saved_plot_name)

    
    @cog_ext.cog_slash(name='plotcombine', guild_ids=guild_ids, description="Combines two plots together into one!", options=options.plotcombine_options)
    async def plotcombine(self, ctx, dataset_name:str, first_plot_name:str, second_plot_name:str, saveas:str=""):
        """Combines two plots into one using plotgenerate!

        Args:
            dataset_name (str): Name of the dataset
            first_plot_name (str): Name of the first saved plot
            second_plot_name (str): Name of the second saved plot
            saveas(str, optional): Name of combination plot to save to dataset
        """
        await self._plotcombine(ctx, dataset_name, first_plot_name, second_plot_name, saveas)

    async def _plotcombine(self, ctx, dataset_name:str, first_plot_name:str, second_plot_name:str, saveas:str="",
     figure_created:bool=False, first_combine:bool=True):
        author = ctx.author

        #Determine if the plots are combination plots
        first_plot_type = await asyncutils.get_saved_plot_type(ctx, dataset_name, first_plot_name)
        second_plot_type = await asyncutils.get_saved_plot_type(ctx, dataset_name, second_plot_name)
        
        new_first_plot_is_combo = False

        if first_plot_type == "combo":
            new_first_plot_is_combo = True

        #Defaults for the various plot settings
        first_create_figure = False
        first_set_common_plot_info = False

        new_figure_created=figure_created
        #If this is the very first plot to be created, create the figure and set the common plot info
        if new_first_plot_is_combo == False and figure_created == False:
            first_create_figure = True
            first_set_common_plot_info = True
            new_figure_created = True

        await self._plotgenerate(ctx, dataset_name, first_plot_name,
         False, first_create_figure, first_set_common_plot_info, False,
          new_figure_created, False)

        await self._plotgenerate(ctx, dataset_name, second_plot_name,
         False, False, False, False,
          True, False)
        
        #Once we have finish combining, print out the plot
        if first_combine == False:
            return
        
        file_name = f'plot_{dataset_name}.png'

        plothelpers.save_and_close(file_name)

        file = discord.File(file_name)

        description=f"Plot combination of {first_plot_name} and {second_plot_name}"
        description+=f"\n\nPlot has been saved as {saveas}! Use `/viewgraphdata {dataset_name}` to view the graph data and `/plotgenerate {dataset_name} {saveas}` to generate the plot again." if saveas != "" else ""
        plot_embed = utils.create_embed(f"Scatterplot for {author.name}", description, discord.Color.dark_orange())
        plot_embed.set_image(url=f"attachment://{file_name}")
        await ctx.send(embed=plot_embed, file=file)
        os.remove(file_name)

        if saveas != "":
            graph_data = {
                "name": "combo",
                "plot1": first_plot_name,
                "plot2": second_plot_name
            }

            await asyncutils.save_graph_data(ctx, dataset_name, saveas, graph_data)
 


    async def _plotgenerate(self, ctx, dataset_name:str, saved_plot_name:str, save_and_close:bool=True,
     create_figure:bool=True, set_common_plot_info:bool=True, send_message:bool=True,
      figure_created:bool=False, first_combine:bool=True):
        
        #Get the graph type
        saved_plot_dict = await asyncutils.get_saved_plot_dict(ctx, dataset_name, saved_plot_name)
        

        #Iterate through the different graph names to determine which type of graph to plot
        graph_name = saved_plot_dict["name"]
        if graph_name == "scatterplot":
            await self._generatescatter(ctx, dataset_name, saved_plot_dict, save_and_close,
             create_figure, set_common_plot_info, send_message)
        elif graph_name == "bargraph":
            await self._generatebar(ctx, dataset_name, saved_plot_dict, save_and_close, create_figure,
            set_common_plot_info, send_message)
        elif graph_name == "combo":
            await self._generatecombo(ctx, dataset_name, saved_plot_dict, figure_created, first_combine)
        else:
            error_msg= f"An error occurred on our end when generating the plot: Incorrect plot name stored in DB. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return

    async def _generatescatter(self, ctx, dataset_name:str, saved_plot_dict, save_and_close:bool, create_figure:bool, set_common_plot_info:bool, send_message:bool):
        keys = ["x_row", "y_row", "x_label", "y_label", "size_row", "color_row_or_one_color", "transparency"]
        values_exist = utils.check_values_exist_for_keys(saved_plot_dict, keys)

        if values_exist == False:
            error_msg = f"An error occured on our end when generating the scatterplot: Plot dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return None

        x_row = saved_plot_dict["x_row"]
        y_row = saved_plot_dict["y_row"]
        x_label = saved_plot_dict["x_label"]
        y_label = saved_plot_dict["y_label"]
        size_row = saved_plot_dict["size_row"]
        color_row_or_one_color = saved_plot_dict["color_row_or_one_color"]
        transparency = saved_plot_dict["transparency"]
        
        scatterplot = Scatterplot()
        await scatterplot._scatterplot(ctx, dataset_name, x_row, y_row, x_label,
         y_label, size_row, color_row_or_one_color, transparency,
         save_and_close=save_and_close, create_figure=create_figure,
          set_common_plot_info=set_common_plot_info, send_message=send_message)

    async def _generatebar(self, ctx, dataset_name:str, saved_plot_dict, save_and_close:bool, create_figure:bool, set_common_plot_info:bool, send_message:bool):
        keys = ["x_row", "height_row", "x_label", "y_label", "width", "bottom_coords_row", "align", "color_row_or_one_color", "label"]
        values_exist = utils.check_values_exist_for_keys(saved_plot_dict, keys)

        if values_exist == False:
            error_msg = f"An error occured on our end when generating the bar graph: Plot dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return None

        x_row = saved_plot_dict["x_row"]
        height_row = saved_plot_dict["height_row"]
        x_label = saved_plot_dict["x_label"]
        y_label = saved_plot_dict["y_label"]
        width = saved_plot_dict["width"]
        bottom_coords_row = saved_plot_dict["bottom_coords_row"]
        align = saved_plot_dict["align"]
        color_row_or_one_color = saved_plot_dict["color_row_or_one_color"]
        label = saved_plot_dict["label"]

        bargraph = BarGraph()
        await bargraph._bargraph(ctx, dataset_name, x_row, height_row, x_label,
         y_label, width, bottom_coords_row, align, color_row_or_one_color, label,
         save_and_close=save_and_close, create_figure=create_figure,
          set_common_plot_info=set_common_plot_info, send_message=send_message)

    async def _generatecombo(self, ctx, dataset_name:str, saved_plot_dict,
     figure_created:bool, first_combine:bool):
        keys = ["plot1", "plot2"]
        values_exist = utils.check_values_exist_for_keys(saved_plot_dict, keys)

        if values_exist == False:
            error_msg = f"An error occured on our end when generating the scatterplot: Plot dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return None

        plot1 = saved_plot_dict["plot1"]
        plot2 = saved_plot_dict["plot2"]

        await self._plotcombine(ctx, dataset_name, plot1, plot2,
          figure_created=figure_created,
            first_combine=first_combine)



def setup(bot):
    bot.add_cog(SavedPlotGeneration(bot))