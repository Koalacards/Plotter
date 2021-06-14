from discord.ext import commands
from discord_slash import cog_ext
import utils
from plotvars import guild_ids
from cogs.helpvars import *

class HelpCommand(commands.Cog):
    @cog_ext.cog_slash(name='help', guild_ids=guild_ids, description="The help command!")
    async def help(self, ctx, subset:str=""):
        """Returns helpful information on the command(s) of Plotter, based on which subset is given!

        Args:
            subset (str, optional): Either a certain section of commands, or a single command to show help for. Defaults to "".
        """
        embed=utils.create_embed(HELP_TITLE, HELP_DESCRIPTION, help_color)
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))