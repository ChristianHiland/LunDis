from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

# API TOKENS
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

roles_List = {
    "General": {"🎭": "Theater", "💻": "Bot Updates", "⚠️": "Big Annoucements", "📰": "News"}
}

# Bot Class
class LunBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=">", intents=intents)
        print("Bot Initialized...")

    @commands.Cog.listener()
    async def on_ready(self):
        print('-------------------------------------')
        print(f'Logged in as: {self.user} (ID: {self.user.id})')
        print(f'Discord.py Version: {discord.__version__}')
        print('-------------------------------------')
        await self.LoadCogs()

    #
    # Events
    #

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return



    #
    # Helpers
    #
    async def LoadCogs(self):
        print("Loading Cogs...")
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py') and filename != '__init__.py':
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    print(f'✅ Successfully loaded cog: {cog_name}')
                except Exception as e:
                    print(f'❌ Failed to load cog {cog_name}.')
                    print(f'[ERROR]: {e}')

lunbot = LunBot()
lunbot.run(token)