import discord
from discord.ext import commands
import db.plotdbfunctions as dbfunc
import utils
import plotvars

class PlotFeatureCommands(commands.Cog):
    @commands.command()
    async def setplottitle(self, ctx, ds_name:str, * plot_title:str):
        plot_title_str = ' '.join(plot_title)
        author = ctx.message.author
        dbfunc.set_plot_title(author.id, ds_name, plot_title_str)
        await ctx.send(f"Plot title of {plot_title_str} has been set for dataset {ds_name}!")
    


def setup(bot):
    bot.add_cog(PlotFeatureCommands(bot))