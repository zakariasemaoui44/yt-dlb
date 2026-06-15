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
    cmd = ["yt-dlp", "--no-playlist", "--js-runtimes", "node:/usr/bin/node"]

   # if os.path.exists(COOKIES_PATH):
    #    cmd += ["--cookies", COOKIES_PATH]

    cmd += extra_args
    cmd.append(url)
    return cmd
    
@app.get("/youtube-test")
def youtube_test(url: str):
    extra_args = [
        "--dump-json", 
        "--no-download",
        "--extractor-args", "youtube:skip=js"  # Skip JS extraction
    ]
    cmd = get_yt_dlp_cmd(url, extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout[:1000],
        "stderr": result.stderr[:1000]
    }

@app.get("/node-test")
def node_test():
    result = subprocess.run(
        ["node", "--version"],
        capture_output=True,
        text=True
    )

    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

@app.get("/ytdlp-version")
def ytdlp_version():
    import subprocess

    result = subprocess.run(
        ["yt-dlp", "--version"],
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr
    }
