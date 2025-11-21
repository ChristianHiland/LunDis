from google.cloud import texttospeech
from Helpers.gemini import Gemini

class STT:
    def __init__(self, filepath):
        self.filepath = filepath

    def Process(self) -> str:
        return Gemini("").TranscribeMP3(self.filepath)

class TTS:
    def __init__(self, text: str):
        self.text = text
        self.file = "Gemini_TTS.mp3"

    def Process(self):
        try:
            client = texttospeech.TextToSpeechClient()
            # 1. Define the input text
            synthesis_input = texttospeech.SynthesisInput(text=self.text)

            # 2. Define the voice parameters
            voice_params = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-News-K"  # Example Wavenet/News voice model
            )

            # 3. Define the audio output format
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # 4. Call the API and await the result
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )

            with open(self.file, "wb") as out:
                out.write(response.audio_content)
        except Exception as e:
            print(f"[ERROR]: {e}")