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
