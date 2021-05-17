import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from confidential import *
from plotvars import guild_ids


client = commands.Bot(command_prefix=".")
slash = SlashCommand(client, override_type=True, sync_commands=True, sync_on_cog_reload=True)


client.remove_command('help')


client.load_extension('cogs.datasetcommands')
client.load_extension('cogs.plotfeaturecommands')
client.load_extension('cogs.plotgenerationcommands')
client.load_extension('cogs.helpcommand')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Plotting | /help"))
    print("Plotter is running")

@slash.slash(name='reloadCog', guild_ids=guild_ids)
async def _reloadCog(ctx, cog):
    if ctx.author.display_name == 'Koalacards':
        client.reload_extension(cog)

client.run(RUN_ID)