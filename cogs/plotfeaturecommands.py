import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import db.plotdbfunctions as dbfunc
import utils
import plotvars
from plotvars import guild_ids

class PlotFeatureCommands(commands.Cog):
    @cog_ext.cog_slash(name='setplottitle', guild_ids=guild_ids)
    async def setplottitle(self, ctx, dataset_name:str, plot_title:str):
        author = ctx.author
        dbfunc.set_plot_title(author.id, dataset_name, plot_title)
        await ctx.send(f"Plot title of {plot_title} has been set for dataset {dataset_name}!")
    


def setup(bot):
    bot.add_cog(PlotFeatureCommands(bot))