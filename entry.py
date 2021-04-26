import discord
from discord.ext import commands
from confidential import *


client = commands.Bot(command_prefix=".")

client.load_extension('cogs.datasetcommands')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".help"))

@client.command(hidden=True)
async def reloadCog(ctx, cog):
    if ctx.message.author.display_name == 'Koalacards':
        client.reload_extension(cog)
    await ctx.message.delete()

client.run(RUN_ID)