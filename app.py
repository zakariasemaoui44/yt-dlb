from fastapi import FastAPI
import subprocess
import os
import tempfile

app = FastAPI()

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
        "--js-runtimes", "nodejs",   # explicitly tell yt-dlp to use node
    ]

    # Use cookies file if available (set via Render env variable)
    cookies_content = os.environ.get("YT_COOKIES")
    if cookies_content:
        # Write cookies to a temp file
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        tmp.write(cookies_content)
        tmp.close()
        cmd += ["--cookies", tmp.name]
    
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
