from dotenv import load_dotenv
from google import genai
import textwrap
import os


API_KEY = os.getenv('GEMINI_TOKEN')
geminiClient = None
if API_KEY != None:
    geminiClient = genai.Client(api_key=API_KEY)

class Gemini:
    def __init__(self, prompt: str = "", max_chars: int = 1950, model_name: str = "gemini-2.5-flash", client = None):
        if client == None:
            self.client = geminiClient
        else:
            self.client = client
        self.prompt = prompt
        self.model_name = model_name
        self.max_chars = max_chars

    def Generate(self) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.prompt
            )
            return response.text
        except Exception as e:
            return f"[Gemini ERROR] {e}"
        
    def BreakLong(self, response: str) -> list[str]:
        chucks = textwrap.wrap(response, self.max_chars, break_long_words=True, replace_whitespace=False)
        if not chucks:
            return ["Nothing to break."]
        return chucks
        
    def FormatHistory(self, history: list[str]) -> str:
        # Rebuild it as a string.
        chatHistory = ""
        chatHistory += "This is a chat from a Discord channel, use the last thing the person said as a prompt, ignore !aiChat as that is the command used to call you, and don't add timestamps. Reply like you're in a converstion, but keep a happy, and crack a few jokes if you see fit. Your name is LunBot to let you know.\n"
        for i in range(0, len(history)):
            chatHistory += history[i] + "\n"
        print(f"[DEBUG]: {chatHistory}")
        return chatHistory

    def ChatGenerate(self, history) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.FormatHistory(history)
            )
            return response.text
        except Exception as e:
            return f"[Gemini ERROR] {e}"
        
    def TranscribeMP3(self, filepath: str) -> str:
        audio_file = self.client.files.upload(file=filepath, config={"mimeType": "audio/wav"})
        # 2. Define the prompt and the file part
        prompt = 'Generate a complete, accurate transcript of the speech in this audio file.'
        
        # 3. Call the API
        print("Generating transcript...")
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, audio_file] # Pass the prompt and the file object
        )
        self.client.files.delete(name=audio_file.name)
        os.remove(filepath)
        return response.text
        

if __name__ == "__main__":
    ai = Gemini("Hi, how are you?")
    print(ai.Generate())