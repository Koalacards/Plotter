import discord
from discord.ext import commands
from discord_slash import cog_ext
from numpy.lib.npyio import save
import utils
import plotvars
from plotvars import guild_ids
import asyncutils
from cogs.plots.scatterplot import Scatterplot
import os

class SavedPlotGeneration(commands.Cog):

    @cog_ext.cog_slash(name='plotgenerate', guild_ids=guild_ids, description="Generates a saved plot from one of yoru datasets!")
    async def plotgenerate(self, ctx, dataset_name:str, saved_plot_name:str):
        """Generates a saved plot from a dataset.

        This method will essentially run the graph command without the user having to input a ton of information

        Args:
            dataset_name (str): name of the dataset
            saved_plot_name (str): Name of the saved plot a user generated earlier
        """

        await self._plotgenerate(ctx, dataset_name, saved_plot_name)

    
    @cog_ext.cog_slash(name='plotcombine', guild_ids=guild_ids, description="Combines two plots together into one!")
    async def plotcombine(self, ctx, dataset_name:str, first_plot_name:str, second_plot_name:str, saveas:str=""):
        """Combines two plots into one using plotgenerate!

        Args:
            dataset_name (str): Name of the dataset
            first_plot_name (str): Name of the first saved plot
            second_plot_name (str): Name of the second saved plot
            saveas(str, optional): Name of combination plot to save to dataset
        """
        await self._plotcombine(ctx, dataset_name, first_plot_name, second_plot_name, saveas)

    async def _plotcombine(self, ctx, dataset_name:str, first_plot_name:str, second_plot_name:str, saveas:str=""):
        author = ctx.author

        await self._plotgenerate(ctx, dataset_name, first_plot_name, False, True, True, False)

        await self._plotgenerate(ctx, dataset_name, second_plot_name, True, False, False, False)
        
        file_name = f'plot_{dataset_name}.png'

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
 


    async def _plotgenerate(self, ctx, dataset_name:str, saved_plot_name:str, save_and_close:bool=True, create_figure:bool=True, set_common_plot_info:bool=True, send_message:bool=True):
        #Get the graph data
        graph_data_dict = await asyncutils.get_graph_data_dictionary(ctx, dataset_name)
        if graph_data_dict is None:
            return

        #Get the saved plot dictionary or error if none is available
        saved_plot_dict = graph_data_dict.get(saved_plot_name, None)

        if saved_plot_dict is None:
            error_msg = f"You do not have a saved plot under the name {saved_plot_name}! Please check the name using `/viewgraphdata {dataset_name}` and try again."
            await ctx.send(embed=utils.error_embed(error_msg))
        

        #Iterate through the different graph names to determine which type of graph to plot
        graph_name = saved_plot_dict["name"]
        if graph_name == "scatterplot":
            await self._generatescatter(ctx, dataset_name, saved_plot_dict, save_and_close, create_figure, set_common_plot_info, send_message)
        elif graph_name == "combo":
            await self._generatecombo(ctx, dataset_name, saved_plot_dict)
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
         save_and_close=save_and_close, create_figure=create_figure, set_common_plot_info=set_common_plot_info, send_message=send_message)

    async def _generatecombo(self, ctx, dataset_name:str, saved_plot_dict):
        keys = ["plot1", "plot2"]
        values_exist = utils.check_values_exist_for_keys(saved_plot_dict, keys)

        if values_exist == False:
            error_msg = f"An error occured on our end when generating the scatterplot: Plot dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return None

        plot1 = saved_plot_dict["plot1"]
        plot2 = saved_plot_dict["plot2"]

        await self._plotcombine(ctx, dataset_name, plot1, plot2)

            
        
    


def setup(bot):
    bot.add_cog(SavedPlotGeneration(bot))