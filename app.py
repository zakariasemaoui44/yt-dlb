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
    cmd = [
        "yt-dlp", 
        "--no-playlist", 
        "--js-runtimes", "deno",  # Using Deno instead of Node.js
        "--remote-components", "ejs:npm",  # Enable EJS from npm
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--sleep-interval", "3",
        "--max-sleep-interval", "5"
    ]

    # Only add cookies if the file exists (commented out for now to avoid cookie issues)
    # if os.path.exists(COOKIES_PATH):
    #     cmd += ["--cookies", COOKIES_PATH]

    cmd += extra_args
    cmd.append(url)
    return cmd

@app.get("/youtube-test")
def youtube_test(url: str):
    extra_args = [
        "--dump-json", 
        "--no-download",
        "--extractor-args", "youtube:player_client=android",  # Use Android client to bypass bot detection
        "--extractor-args", "youtube:skip=js",  # Skip JS challenges
        "--sleep-interval", "3",
        "--max-sleep-interval", "5"
    ]
    cmd = get_yt_dlp_cmd(url, extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout[:2000] if result.stdout else "",
        "stderr": result.stderr[:2000] if result.stderr else ""
    }

@app.get("/youtube-test-simple")
def youtube_test_simple(url: str):
    """Simpler test without extra parameters"""
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--js-runtimes", "deno",
        "--remote-components", "ejs:npm",
        "--dump-json",
        "--no-download",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "return_code": result.returncode,
        "stdout": result.stdout[:2000] if result.stdout else "",
        "stderr": result.stderr[:2000] if result.stderr else ""
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

@app.get("/deno-test")
def deno_test():
    result = subprocess.run(
        ["deno", "--version"],
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
    result = subprocess.run(
        ["yt-dlp", "--version"],
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr
    }
