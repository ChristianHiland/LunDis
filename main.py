from Helpers.Gemini import Gemini
from discord.ext import commands
from dotenv import load_dotenv
from google import genai
from time import sleep
import discord
import os


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GEM_API = os.getenv('GEMINI_TOKEN')
DEBUG = False
if os.getenv("DEBUG") == "true":
    DEBUG = True

gemini_client = None

try:
    gemini_client = genai.Client(api_key=GEM_API)
except Exception as e:
    print(f"Failed to initialize Gemini Client: {e}")
    gemini_client = None # Handle case where client might not be available

intents = discord.Intents.default()
intents.message_content = True

# Server Data
lock_channels = {0: [8280938290138208309,3727389193798237], 1438330109311586407: [1438502099473272882, 1438502146319581254, 1438865371557003422, 1438333567053725837]}

# Making a connection to Discord
bot = commands.Bot(command_prefix='>', intents=intents)

#
# Helper Functions
#

def SaveChat(full_history, channel) -> str:
    """Helper Function to save chat history to a file."""
    filename = f"Data/{channel.name}_history.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_history)
    return filename


async def load_cogs():
    """Asynchronously loads all cog files from the cogs directory."""
    print("Starting cog loading process...")
    
    for filename in os.listdir('./cogs'):
        # Only process Python files and skip the __init__.py file
        if filename.endswith('.py') and filename != '__init__.py' and filename != 'gemini.py':
            # Construct the dot-notation path: 'cogs.filename_without_py'
            cog_name = f'cogs.{filename[:-3]}'
            try:
                # The crucial part: await bot.load_extension()
                await bot.load_extension(cog_name)
                print(f'✅ Successfully loaded cog: {cog_name}')
            except Exception as e:
                # Print the exact error if a cog fails to load
                print(f'❌ Failed to load cog {cog_name}.')
                print(f'[ERROR]: {e}')

# Event Bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    # >>> 1. Loading Cogs <<<<
    await load_cogs()
# User Replying to bot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # --- BOT MENTION LOGIC ---
    
    # 1. Check if the message mentions the bot user
    if bot.user in message.mentions:
        
        # 2. Optionally, check if the mention is the *only* thing in the message
        # This prevents the bot from replying if it's mentioned inside a longer text.
        # .strip() removes whitespace, .replace() removes the mention itself.
        is_only_mention = message.content.strip() == bot.user.mention

        if is_only_mention:
            
            # 3. Construct the response
            # You can give instructions, status, or a simple greeting
            
            response = (
                f"Hello, My Fellow HUMANS (Maybe Humans)! 👋\n"
                f"My prefix is `$`. Try typing `$help` to see what I can do."
            )
            
            # Use message.reply() to reply directly to the mention
            await message.reply(response) 
            
            # Optional: If the bot is only supposed to respond to the mention 
            # and not try to process it as a command, you can return here:
            # return

    # Check if the message was a reply.
    if message.reference and message.reference.message_id:
        # Try to fetch the message that was repiled to.
        try:
            original_message = await message.channel.fetch_message(message.reference.message_id)
        except discord.NotFound:
            original_message = None

        # Checking to see if the message replied to was from the bot.
        if original_message and original_message.author == bot.user:
            # Get the past messages
            history_list = []
            
            # The channel object is retrieved from the context (ctx.channel)
            channel = message.channel 
            async for message in channel.history(limit=100):
                formatted_message = (
                    f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"**{message.author.display_name}**: {message.content}"
                )
                history_list.append(formatted_message)
            history_list.reverse()

            # Make Reply
            ai = Gemini("")
            await message.reply(ai.ChatGenerate(history_list))
    await bot.process_commands(message)

#
# Helper Discord Commands
#

@bot.command()
@commands.has_permissions(administrator=True) # Optional: Limit this to admins
async def purgeChannel(ctx):
    await ctx.send("Deleting Channel Messages...")
    sleep(2)
    for i in range(0,3):
        await ctx.send(f"In {i}...")
        sleep(1)

    await ctx.channel.purge()

@bot.command()
async def maintenance(ctx, mode: bool = True, time_mins: int = 25):
    if mode:
        await ctx.send("everyone SERVER IS UNDER MAINTENANCE PLEASE DO NOT INTERACT WITH THIS BOT OR BOT CHANNELS!")
        await ctx.send(f"[DEBUG]: LUNBOT IS UNDER MAINTENANCE, BOT MAY NOT WORK AFTER AND MAY NOT WORK DURING MAINTENANCE. BOT WILL BE TURNED OFF AND ON DURING THIS PROCESS FOR DEBUG. \nPlanned Maintenance Will Take: {time_mins} mins")

        # Locking Channel Messaging
        everyone_role = ctx.guild.default_role

        current_perms = ctx.channel.overwrites_for(everyone_role)
        if current_perms.send_messages is False:
            return await ctx.send("🔒 This channel is already locked.")
        
        try:
            await ctx.channel.set_permissions(
                everyone_role,
                send_messages=False,
                reason=f"Channel locked by {ctx.author.name}"
            )
            await ctx.send("🔒 Channel locked. Users can no longer type here.")
        except discord.Forbidden:
            await ctx.send("❌ I do not have permission to modify channel permissions.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")
    else:
        await ctx.send("everyone Server is now in normal working operation. This bot is now able to be used. Please do note it might be work correctly.")
        # Locking Channel Messaging
        everyone_role = ctx.guild.default_role

        current_perms = ctx.channel.overwrites_for(everyone_role)
        
        try:
            await ctx.channel.set_permissions(
                everyone_role,
                send_messages=True,
                reason=f"Channel locked by {ctx.author.name}"
            )
            await ctx.send("🔒 Channel unlocked. Users can continue typing here.")
        except discord.Forbidden:
            await ctx.send("❌ I do not have permission to modify channel permissions.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

# Locking Server Channels
@bot.command()
async def lockdown(ctx, mode: str = "full"):
    if mode.lower() == "full":
        guild_id = ctx.guild.id

        everyone_role = ctx.guild.default_role
        current_perms = ctx.channel.overwrites_for(everyone_role)
        print(f"Server ID: {guild_id}")
        for channelID in lock_channels[guild_id]:
            try:
                if current_perms.send_messages:
                    channel = bot.get_channel(channelID)
                    if channel is None:
                        await ctx.send(f"[ERROR]: Couldn't find channel with ID: {channelID}")
                    else:
                        await ctx.channel.set_permissions(everyone_role, send_messages=False, reason="Channel Locked.")
                        await channel.send("🔒 Channel locked. Users can no longer type here.")
                else:
                    channel = bot.get_channel(channelID)
                    if channel is None:
                        await ctx.send(f"[ERROR]: Couldn't find channel with ID: {channelID}")
                    else:
                        await channel.set_permissions(everyone_role, send_messages=True, reason="Channel unlocked.")
                        await channel.send("🔒 Channel unlocked. Users can continue typing here.")
            except Exception as e:
                await ctx.send(f"[DISCORD ERROR]: {e}")

bot.run(token)