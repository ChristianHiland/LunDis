import subprocess
import os

class YouTube:
    def __init__(self, url: str, output: str = "./ytDownloads"):
        self.url = url
        self.output = output

    def Download(self):
        print(f"Starting download for {self.url}")
        # Getting Cookie file path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        cookie_filepath = os.path.join(BASE_DIR, "cookies.txt")
        try:
            args = [
                "yt-dlp",
                "--cookies",
                cookie_filepath,
                "--extract-audio",
                "--audio-format", "mp3",
                "--output", self.output + "/audio.mp3",
                self.url
            ]
            result = subprocess.run(args, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"Successfully downloaded and converted {self.url} to MP3.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[YT ERROR]: {result.stderr}")
            return False
        except Exception as e:
            print(f"[YT ERROR]: An error occurred: {e}")
            return False