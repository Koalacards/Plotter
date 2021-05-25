from discord.ext import commands
from discord_slash import cog_ext
import utils
from plotvars import guild_ids
from cogs.helpvars import *

class HelpCommand(commands.Cog):
    @cog_ext.cog_slash(name='help', guild_ids=guild_ids)
    async def help(self, ctx, subset:str=""):
        embed=utils.create_embed(HELP_TITLE, HELP_DESCRIPTION, help_color)
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))