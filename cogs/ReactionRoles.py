from discord.ext.commands import Context
from discord.ext import commands
import discord

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generalRoleID = None
    @commands.command()
    async def GeneralRoles(self, ctx: Context):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You do not have the permissions to do this!", ephemeral=True)
            return
        
        await ctx.defer(ephemeral=True)
        # Set up role message.
        text = ("React to the Emojis to assign a role\n\n"
                    "🎭: Theater Updates & Planning\n"
                    "💻: Bot Big Updates\n"
                    "⚠️: Big annoucements, School Updates\n"
                    "📰: News"
        )

        embed = discord.Embed(title="General Roles.", description=text, color=discord.Color.blurple())
        message = await ctx.send(embed=embed)
        emojis = ['🎭', '💻', '⚠️', '📰']

        for emoji in emojis:
            await message.add_reaction(emoji)

        self.generalRoleID = message.id



async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))