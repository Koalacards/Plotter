import discord
from discord.ext import commands
import db.plotdbfunctions as dbfunc

class DataSetCommands(commands.Cog):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command()
    async def create2Ddataset(self, ctx, name:str):
        author = ctx.message.author
        try:
            dbfunc.set_dataset(author.id, name, "2D")
            await ctx.send(f"2D dataset `{name}` has been created!")
        except:
            await ctx.send("You already have a dataset with the same name!")

    @commands.command()
    async def removedataset(self, ctx, name:str):
        author = ctx.message.author
        num_removed = dbfunc.remove_dataset(author.id, name)
        if num_removed == 0:
            await ctx.send("There is no dataset with this name to remove!")
        else:
            await ctx.send(f"Dataset `{name}` successfully removed!")
    


def setup(bot):
    bot.add_cog(DataSetCommands(bot))