import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from confidential import *
import plotvars
import utils
from plotvars import guild_ids


client = commands.Bot(command_prefix=".")
slash = SlashCommand(client, override_type=True, sync_commands=True, sync_on_cog_reload=True)


client.remove_command('help')


client.load_extension('cogs.datasetcommands')
client.load_extension('cogs.plotfeaturecommands')
client.load_extension('cogs.plots.scatterplot')
client.load_extension('cogs.helpcommand')
client.load_extension('cogs.savedplotgeneration')
client.load_extension('cogs.utilitycommands')
client.load_extension('cogs.plots.bargraph')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Plotting | /help"))
    print("Plotter is running")

@slash.slash(name='reloadCog', guild_ids=guild_ids)
async def reloadCog(ctx, cog):
    if ctx.author.display_name == 'Koalacards':
        client.reload_extension(cog)
        await ctx.send("Cog has been reloaded")
    else:
        await ctx.send("You are not my creator")


client.run(RUN_ID)