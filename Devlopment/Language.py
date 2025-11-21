from Helpers.Processing import STT, TTS
from discord.ext import commands
from Helpers.gemini import Gemini
import discord
import os

class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_id_lisner = None
        self.audio_channel = None
        #self.audio_log = ["SYSTEM: Your an AI helping someone learn a language"]
        self.vc = None

    @commands.command()
    async def LanguageLearn(self, ctx, language: str):
        if not ctx.author.voice:
            return await ctx.send("Connect to audio channel 1st")
        
        self.audio_channel = ctx.author.voice.channel
        self.user_id_lisner = ctx.author.id

        # Try to connect
        try:
            self.vc = await self.audio_channel.connect()
            # Make a audio handler
            # Start the recording stream. 
            # The 'pycord_after_recording' callback function is called when recording stops.
            self.vc.start_recording(
                discord.sinks.MP3Sink(), # Use MP3 format (other sinks are available)
                self.Process_And_Reply, 
                ctx.channel # Pass the channel context to the callback
            )
            await ctx.send(f"🎙️ Now recording audio in **{self.audio_channel.name}**. Use `!stop` to finish.")
        except discord.ClientException:
            self.vc = ctx.voice_client
        except Exception as e:
            return await ctx.send(f"[ERROR]: {e}")

    @commands.command()
    async def Process_And_Reply(self, sink, channel, *args):
        # This function runs after vc.stop_recording() is called.
        # Get the recorded audio data for each user
        recorded_users = []
        
        # 'sink.audio_data' holds the recorded audio streams, keyed by user ID
        async for user_id, audio in sink.audio_data.items():
            if user_id == self.user_id_lisner:
                user = channel.guild.get_member(user_id)
                # Save the audio data to a file for each user
                user_filename = f"Recordings/{user.name}_{channel.guild.name}_recording.mp3"
                with open(user_filename, 'wb') as f:
                    f.write(audio.file.read())
                    
                recorded_users.append(user.display_name)
                # Process Audio Into Text
                text = self.STT(user_filename)
                #self.audio_log.append(text)
                await channel.send(f"STT Got: {text}")
                # Send the file (or log it)
                await channel.send(f"Finished recording audio from **{user.display_name}**.", 
                                file=discord.File(user_filename))
                
                # Reply
                self.AIReply(text)

        if recorded_users:
            await channel.send(f"Recording stopped. Audio saved for: {', '.join(recorded_users)}")
        else:
            await channel.send("Recording stopped, but no audio was detected.")

    @commands.command()
    async def TestResponse(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("Connect to audio channel 1st")
        
        self.audio_channel = ctx.author.voice.channel
        self.user_id_lisner = ctx.author.id
        try:
            self.vc = await self.audio_channel.connect()
            text = "Hello, I'm testing Text to Speech"
            await self.AIReply(text)
        except Exception as e:
            import traceback
            print(f"{traceback.format_exc} {traceback.format_exception}")
            print(f"fail with {e}")


    async def AIReply(self, user_text):
        # Make AI Response
        try:
            response = Gemini("").ChatGenerate(["SYSTEM: You are an AI, that is helping someone learn a language in this case it being Korean."])
            print(response)
            self.TTS(response)
        except Exception as e:
            print(f"Failed to get response\n{e}")
        audio_source = discord.FFmpegOpusAudio("Gemini_TTS.mp3")

        self.vc.play(audio_source, after=lambda e: print(f'Player error: {e}') if e else None)

    async def STT(self, filepath) -> str:
        stt = STT(filepath)
        text = await stt.Process()
        print(f"Got this from Speech: {text}")
        return text
    def TTS(self, text):
        tts = TTS(text)
        tts.Process()

async def setup(bot):
    await bot.add_cog((Language(bot)))