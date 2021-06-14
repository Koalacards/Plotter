import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import db.plotdbfunctions as dbfunc
import utils
import plotvars
from plotvars import guild_ids

class PlotFeatureCommands(commands.Cog):
    @cog_ext.cog_slash(name='setplottitle', guild_ids=guild_ids, description="Set the plot title for your dataset!")
    async def setplottitle(self, ctx, dataset_name:str, plot_title:str):
        """Sets a plot title for your dataset.

        Args:
            dataset_name (str): Name of the dataset
            plot_title (str): Title of the plot
        """
        author = ctx.author
        dbfunc.set_plot_title(author.id, dataset_name, plot_title)
        title=f"Plot title of `{plot_title}` has been set for dataset {dataset_name}!"
        description=""
        colour=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, colour))
    
    @cog_ext.cog_slash(name='setaxisboundaries', guild_ids=guild_ids, description="Set specific lengths for your X and Y axes! (Overrides axis options)")
    async def setaxisboundaries(self, ctx, dataset_name:str, minimum_x:float, maximum_x:float, minimum_y: float, maximum_y: float):
        """Sets specific axis boundaries (minimums and maximums for x and y) for a specific dataset.

        Args:
            dataset_name (str): Name of the dataset
            minimum_x (float): Minimum X value for the axis
            maximum_x (float): Maximum X value for the axis
            minimum_y (float): Minimum Y value for the axis
            maximum_y (float): Maximum Y value for the axis
        """
        try:
            author = ctx.author
            bounds = [float(minimum_x), float(maximum_x), float(minimum_y), float(maximum_y)]
            dbfunc.set_axis_info(author.id, dataset_name, str(bounds))
            title=f"Axis boundaries `{str(bounds)}` have been set for dataset {dataset_name}!"
            description=""
            colour=discord.Color.green()
            await ctx.send(embed=utils.create_embed(title, description, colour))
        except:
            description=f"One of your boundary inputs was not a float. Please try again or reference `/help setaxisboundaries` for more information."
            await ctx.send(embed=utils.error_embed(description))
        
    @cog_ext.cog_slash(name='setaxisoption', guild_ids=guild_ids, description="Set axis mode to a certain option! (Overrides axis boundaries)")
    async def setaxisoption(self, ctx, dataset_name:str, option:str):
        """Sets a specific axis option for a dataset.

        Options are based on the axis options that matplotlib has.

        Args:
            dataset_name (str): Name of the dataset
            option (str): Axis option
        """
        author = ctx.author
        correct_option=False
        if option == "on":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "off":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "equal":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "scaled":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "tight":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "auto":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "image":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        elif option == "square":
            dbfunc.set_axis_info(author.id, dataset_name, option)
            correct_option=True
        
        if correct_option:
            title=f"Axis option {option} has been set for dataset {dataset_name}!"
            description=""
            colour=discord.Color.green()
            await ctx.send(embed=utils.create_embed(title, description, colour))
        else:
            description=f"Your option was not one of the valid options (either on, off, equal, scaled, tight, auto, image, or square). Please try again or reference `/help setaxisoption` for more information."
            await ctx.send(embed=utils.error_embed(description))


def setup(bot):
    bot.add_cog(PlotFeatureCommands(bot))