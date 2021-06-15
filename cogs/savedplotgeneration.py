import discord
from discord.ext import commands
from discord_slash import cog_ext
import utils
import plotvars
from plotvars import guild_ids
import asyncutils
from cogs.plots.scatterplot import Scatterplot as scatterplot
import cogs.plots.scatterplot as scatter
import cogs.plots.plothelpers as plothelpers
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
    async def plotcombine(self, ctx, dataset_name:str, first_plot_name:str, second_plot_name:str):
        """Combines two plots into one using plotgenerate!

        Args:
            dataset_name (str): Name of the dataset
            first_plot_name (str): Name of the first saved plot
            second_plot_name (str): Name of the second saved plot
        """
        author = ctx.author

        await self._plotgenerate(ctx, dataset_name, first_plot_name, False, True, True)

        await self._plotgenerate(ctx, dataset_name, second_plot_name, True, False, False)
        
        file_name = f'plot_{dataset_name}.png'

        file = discord.File(file_name)

        description=f"Plot combination of {first_plot_name} and {second_plot_name}"
        plot_embed = utils.create_embed(f"Scatterplot for {author.name}", description, discord.Color.dark_orange())
        plot_embed.set_image(url=f"attachment://{file_name}")
        await ctx.send(embed=plot_embed, file=file)
        os.remove(file_name)
 


    async def _plotgenerate(self, ctx, dataset_name:str, saved_plot_name:str, save_and_close:bool=True, create_figure:bool=True, set_common_plot_info:bool=True):
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
            await self._generatescatter(ctx, dataset_name, saved_plot_dict, save_and_close, create_figure, set_common_plot_info)
        else:
            error_msg= f"An error occurred on our end when generating the plot: Incorrect plot name stored in DB. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(error_msg))
            return

    async def _generatescatter(self, ctx, dataset_name:str, saved_plot_dict, save_and_close:bool, create_figure:bool, set_common_plot_info:bool):
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
            
        if save_and_close == True and create_figure == True and set_common_plot_info == True:
            await scatterplot._scatterplot(scatterplot, ctx, dataset_name, x_row, y_row, x_label, y_label, size_row, color_row_or_one_color, transparency)
        else:
            #Do the scatterplot more manually using the modularized methods/functions
            answer_dict = await scatter._sanitize_scatterplot_inputs(ctx, dataset_name, x_row, y_row, size_row, color_row_or_one_color, transparency)
            if answer_dict is None:
                return None

            values_exist = utils.check_values_exist_for_keys(answer_dict, ["x", "y", "size", "color", "alpha"])

            if values_exist == False:
                error_msg = f"An error occured on our end when generating the scatterplot: Answer dictionary does not have one or more necessary values. Please use `/report` to report the issue or get help in our support server: {plotvars.support_discord_link}"
                await ctx.send(embed=utils.error_embed(error_msg))
                return None

            x = answer_dict["x"]
            y = answer_dict["y"]
            size = answer_dict["size"]
            color = answer_dict["color"]
            alpha = answer_dict["alpha"]

            if create_figure:
                plothelpers.create_figure()
            
            scatter.create_plot(x, y, size, color, alpha)

            if set_common_plot_info:
                plothelpers.set_common_plot_info(ctx.author, dataset_name, x_label, y_label)

            if save_and_close:
                file_name = f'plot_{dataset_name}.png'
                plothelpers.save_and_close(file_name)

            
        
    


def setup(bot):
    bot.add_cog(SavedPlotGeneration(bot))