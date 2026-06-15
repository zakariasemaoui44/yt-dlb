from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

COOKIES_PATH = os.path.join(os.path.dirname(__file__), "cookies.txt")

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/test")
def test():
    result = subprocess.run(
        ["yt-dlp", "--version"],
        capture_output=True,
        text=True
    )
    return {"yt_dlp_version": result.stdout.strip()}

def get_yt_dlp_cmd(url: str, extra_args: list = []):
    cmd = ["yt-dlp", "--no-playlist", "--js-runtimes", "node"]

    if os.path.exists(COOKIES_PATH):
        cmd += ["--cookies", COOKIES_PATH]

    cmd += extra_args
    cmd.append(url)
    return cmd

@app.get("/youtube-test")
def youtube_test():
    cmd = get_yt_dlp_cmd(
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        ["--dump-json", "--no-download"]
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout[:1000],
        "stderr": result.stderr[:1000]
    }
