from discord.ext import commands
from cogs.gemini import Gemini
import discord

class AI(commands.Cog):
    # Cogs need to have the bot instance when init.
    def __init__(self, bot, gemini_client):
        self.bot = bot
        self.max_chars = 1950
        self.gemini_client = gemini_client

    # Defien Commands within a class, they must have self.
    @commands.command(name="aiPrompt")
    async def aiPrompt(self, ctx, prompt: str, model: str = "gemini-2.5-flash"):
        """Using a prompt send it to Gemini to get a response, you can also change the model of Gemini."""
        await ctx.send(f"Thinking...")
        ai = Gemini(prompt, model, gemini_client=self.gemini_client)
        response = ai.Generate()
        if len(response) > self.max_chars:
            chunks = ai.BreakLong(response)
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)

    @commands.command(name="aiChat")
    async def aiChat(self, ctx, limit: int =100):
        """Uses the whole channel history to response, make sure to leave your last message as a prompt for it to answer."""
        history_list = []
        channel = ctx.channel
        async for message in channel.history(limit=limit):
            formatted_message = f"**{message.author.display_name}**: {message.content}"
            if formatted_message.startswith(f"{message.author.display_name}: >aiChat"):
                pass
            else:
                history_list.append(formatted_message)
        history_list.reverse()

        # Getting response
        await ctx.send("Thinking...")
        ai = Gemini("", gemini_client=self.gemini_client)
        await ctx.send(ai.ChatGenerate(history_list))

# Update the setup function to accept keyword arguments (optional)
# and ensure the client is passed when the cog is instantiated.
async def setup(bot, **kwargs):
    # Retrieve the client passed during load_extension
    gemini_client = kwargs.get('gemini_client')
    
    if not gemini_client:
        # Fallback or error handling if client wasn't passed
        print("Error: Gemini client not passed to AI cog.")
        return
        
    await bot.add_cog(AI(bot, gemini_client))