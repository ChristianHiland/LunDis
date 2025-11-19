from discord.ext.commands import Context
from discord.ext import commands
from Helpers.YT import YouTube
import discord

voice_history = []

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Voice Vars
        self.currentChannel = None
        self.user_id = None
        self.vc = None

    @commands.command()
    async def JoinVoice(self, ctx: Context):
        """Let the bot join the current VC you're in."""
        # Check if user is in a channel.
        if not ctx.author.voice:
            return await ctx.send("Connect to a audio channel before running this command.")
        
        self.currentChannel = ctx.author.voice.channel
        self.user_id = ctx.author.id

        # Try to connect.
        try:
            self.vc = await self.currentChannel.connect()
        except discord.ClientException:
            self.vc = ctx.voice_client
        except Exception as e:
            return await ctx.send(f"[Voice.py ERROR]: {e}")

    @commands.command()
    async def LeaveVoice(self, ctx: Context):
        """Disconnect bot from current VC."""
        await ctx.send("Disconnecting from VC")
        self.bot.voice_client.disconnect()
        self.vc = None
        self.user_id = None
        self.currentChannel = None

    @commands.command()
    async def PlayYT(self, ctx: Context, url: str):
        """Allow the bot to get a YT Video and start playing it."""
        await ctx.send("Please wait while I download the video...")
        result = YouTube(url=url).Download()
        if not result:
            await ctx.send("Cookies has gone bad or something else went wrong.")
        else:
            await ctx.send("Now playing.")
            await self.PlayOnChannel("ytDownloads/audio.mp3")

    @commands.command()
    async def TestAudioPlayback(self, ctx: Context):
        """Debug: Test Audio Playback on a channel"""
        await ctx.send("Testing audio playback...")
        result = await self.PlayOnChannel("Recordings/Test.wav")
        if not result:
            await ctx.send("Connect to a channel before testing.")

    async def PlayOnChannel(self, filename: str):
        """Play a audio file in a audio channel."""
        if filename.endswith(".wav"):
            audio_source = discord.FFmpegPCMAudio(filename)
        elif filename.endswith(".mp3"):
            audio_source = discord.FFmpegOpusAudio(filename)
        self.vc.play(audio_source, after=lambda e: print(f"player error: {e}") if e else None)
        return True

async def setup(bot):
    await bot.add_cog(Voice(bot))