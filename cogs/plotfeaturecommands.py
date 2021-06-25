import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import db.plotdbfunctions as dbfunc
import utils
import asyncutils
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

    @cog_ext.cog_slash(name='setxticks', guild_ids=guild_ids, description="Set the x tick numbers and labels!")
    async def setxticks(self, ctx, dataset_name:str, ticks_row:str, labels_row:str="", remove_ticks:str="false"):
        """Sets the x ticks of a graph, along with corresponding (optional) labels.

        The ticks must be a row of numbers, and the labels is a row of strings.

        Args:
            dataset_name (str): Name of the database
            ticks_row (str): Row of data in database corresponding to the x ticks
            labels_row (str, optional): Row of data in the database corresponding to the x labels. Defaults to "".

        Returns:
            [type]: [description]
        """
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
        if datadict is None:
            return None

        #Initialize dictionary
        ticksdict = {}

        if remove_ticks != "on":
            #Get the list of numbers for the x ticks and add it to the dictionary
            tick_values= await asyncutils.verify_rows_are_rows_of_numbers(ctx, dataset_name, datadict, [ticks_row])
            if tick_values is None:
                return
            x_ticks = tick_values[0]

            ticksdict["ticks"] = x_ticks

            #Get the list of strings for the x labels and add to the dictionary (if applicable)
            if labels_row != "":
                tick_labels = await asyncutils.verify_rows_exist_in_dataset(ctx, dataset_name, datadict, [labels_row])
                if tick_labels is None:
                    return
                x_labels = tick_labels[0]

                #Convert labels list to list of strings
                x_labels_as_strlist = []
                for label in x_labels:
                    x_labels_as_strlist.append(str(label))

                if len(x_ticks) != len(x_labels_as_strlist):
                    description=f"Your ticks and lables rows must be of the same length!"
                    await ctx.send(embed=utils.error_embed(description))
                    return
                
                ticksdict["labels"] = x_labels_as_strlist
        
        #Write ticks dictionary to database
        written = await asyncutils.log_xticks_to_database(ctx, dataset_name, ticksdict)
        if written == False:
            return

        title=f"X Ticks (and possible labels) for dataset `{dataset_name}` have been updated! To view the values use `/viewdata {dataset_name}`"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))

    @cog_ext.cog_slash(name='setyticks', guild_ids=guild_ids, description="Set the y tick numbers and labels!")
    async def setyticks(self, ctx, dataset_name:str, ticks_row:str, labels_row:str="", remove_ticks:str="false"):
        """Sets the y ticks of a graph, along with corresponding (optional) labels.

        The ticks must be a row of numbers, and the labels is a row of strings.

        Args:
            dataset_name (str): Name of the database
            ticks_row (str): Row of data in database corresponding to the y ticks
            labels_row (str, optional): Row of data in the database corresponding to the y labels. Defaults to "".

        Returns:
            [type]: [description]
        """
        #Get the data
        datadict = await asyncutils.get_data_dictionary(ctx, dataset_name)
        if datadict is None:
            return None

        #Initialize dictionary
        ticksdict = {}

        if remove_ticks != "on":
            #Get the list of numbers for the x ticks and add it to the dictionary
            tick_values= await asyncutils.verify_rows_are_rows_of_numbers(ctx, dataset_name, datadict, [ticks_row])
            if tick_values is None:
                return
            y_ticks = tick_values[0]

            ticksdict["ticks"] = y_ticks

            #Get the list of strings for the x labels and add to the dictionary (if applicable)
            if labels_row != "":
                tick_labels = await asyncutils.verify_rows_exist_in_dataset(ctx, dataset_name, datadict, [labels_row])
                if tick_labels is None:
                    return
                y_labels = tick_labels[0]

                #Convert labels list to list of strings
                y_labels_as_strlist = []
                for label in y_labels:
                    y_labels_as_strlist.append(str(label))

                if len(y_ticks) != len(y_labels_as_strlist):
                    description=f"Your ticks and lables rows must be of the same length!"
                    await ctx.send(embed=utils.error_embed(description))
                    return
                
                ticksdict["labels"] = y_labels_as_strlist
        
        #Write ticks dictionary to database
        written = await asyncutils.log_yticks_to_database(ctx, dataset_name, ticksdict)
        if written == False:
            return

        title=f"Y Ticks (and possible labels) for dataset `{dataset_name}` have been updated! To view the values use `/viewdata {dataset_name}`"
        description=""
        color=discord.Color.green()
        await ctx.send(embed=utils.create_embed(title, description, color))


def setup(bot):
    bot.add_cog(PlotFeatureCommands(bot))