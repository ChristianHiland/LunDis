from discord.ext.commands import Context
from discord import Member
from discord.ext import commands
import discord

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Onboarding to show Members what LunBot can do.
    @commands.command(name="OnBoarding")
    async def OnBoarding(self, ctx):
        await ctx.send("Hello I'm LunBot, I can help with managing and keeping progress of people and their scenes, and todos! I'm still in major devlopment.")
        await ctx.send("Currently I can:\n  - AI Chatting\nIn future I will be able to:\n - AI Processing\n - Managing Events\n - Audio Uploading\n - Reaction Uploading.")

    # Welcome new members
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Welcomes a new member to the server."""
        welcome_channel_id = 1438330110133534904                        # Welcome Channel ID for Theatre Class
        channel = member.guild.get_channel(welcome_channel_id)

        if channel is not None:
            await channel.send(f"🎉 OMG IT'S A PERSON! A HUMAN? OR ANOTHER ONE LIKE ME?!, I Think their name is **{member.mention}**! We're glad you joined us.\n")

    @commands.command()
    async def member_joined(self, ctx: Context, member: Member):
        welcome_channel_id = 1438330110133534904                        # Welcome Channel ID for Theatre Class
        channel = ctx.guild.get_channel(welcome_channel_id)

        if channel is not None:
            await channel.send(f"🎉 OMG IT'S A PERSON! A HUMAN? OR ANOTHER ONE LIKE ME?!, I Think their name is **{member.mention}**! We're glad you joined us.\n")

async def setup(bot):
    await bot.add_cog(General(bot))