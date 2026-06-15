from fastapi import FastAPI
import subprocess

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

    return {
        "yt_dlp_version": result.stdout.strip()
    }

@app.get("/youtube-test")
def youtube_test():

    result = subprocess.run(
        [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            "https://www.youtube.com/watch?v=5PgVkZRgAHo"
        ],
        capture_output=True,
        text=True
    )

    return {
        "return_code": result.returncode,
        "stdout": result.stdout[:1000],
        "stderr": result.stderr[:1000]
    }
