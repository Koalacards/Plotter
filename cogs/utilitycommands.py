import re
from peewee import _BoundTableContext
import plotvars
from plotvars import guild_ids
import utils
import discord
from discord.ext import commands
from discord_slash import cog_ext

class UtilityCommands(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot=bot

    @cog_ext.cog_slash(name='report', guild_ids=guild_ids, description="Report a bug directly to Plotter staff!")
    async def report(self, ctx, report:str):
        report_channel = self.bot.get_channel(plotvars.reports_channel)
        if report_channel is None:
            description=f"An Error happened on our end: report channel not found. Please report this issue to our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(description))
            return
        else:
            title=f"New Bug Report From {ctx.author.name} (user ID: {ctx.author.id})"
            colour = discord.Color.dark_orange()
            await report_channel.send(embed=utils.create_embed(title, report, colour))

            await ctx.send(embed=utils.create_embed("Thank you! Your bug report has been sent.", "", colour))

    @cog_ext.cog_slash(name='suggest', guild_ids=guild_ids, description="Suggest a new idea directly to Plotter staff!")
    async def suggest(self, ctx, suggestion:str):
        suggestion_channel = self.bot.get_channel(plotvars.suggestion_channel)
        if suggestion_channel is None:
            description=f"An Error happened on our end: Suggestion channel not found. Please report this issue to our support server: {plotvars.support_discord_link}"
            await ctx.send(embed=utils.error_embed(description))
            return
        else:
            title=f"New Feature Suggestion From {ctx.author.name} (user ID: {ctx.author.id})"
            colour = discord.Color.dark_orange()
            await suggestion_channel.send(embed=utils.create_embed(title, suggestion, colour))

            await ctx.send(embed=utils.create_embed("Thank you! Your feature suggestion has been sent.", "", colour))
    
    @cog_ext.cog_slash(name="invite", guild_ids=guild_ids, description="Get a bot invite to add to your server!")
    async def invite(self, ctx):
        embed= discord.Embed(
            title="Add Plotter to your Server!",
            url="https://discord.com/api/oauth2/authorize?client_id=836212383847809075&permissions=2147535872&scope=bot%20applications.commands",
            colour=discord.Color.dark_orange()
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="support", guild_ids=guild_ids, description="Get link to Plotter's Support Server!")
    async def support(self, ctx):
        embed= discord.Embed(
            title="Join Plotter's Support Server!",
            url=plotvars.support_discord_link,
            colour=discord.Color.dark_orange()
        )

        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(UtilityCommands(bot))