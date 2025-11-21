from discord.ext.commands import Context
from discord.ext import commands
from time import sleep
import discord

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purgeChannel(self, ctx: Context):
        if ctx.author.guild_permissions.administrator:
            await ctx.send("Deleting Channel Messages...")
            counter = 3
            while counter != 0:
                await ctx.send(f"In {counter}...")
                counter -= 1
                sleep(1)
            await ctx.channel.purge()
        else:
            await ctx.send("You don't have permissions to do this.")

    

    
async def setup(bot):
    await bot.add_cog(Management(bot))