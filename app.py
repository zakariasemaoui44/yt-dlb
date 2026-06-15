from fastapi import FastAPI
import subprocess
import os
import json

app = FastAPI()

COOKIES_PATH = os.path.join(os.path.dirname(__file__), "www.youtube.com_cookies.txt")

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

def get_yt_dlp_cmd(url: str, extra_args: list = None):
    if extra_args is None:
        extra_args = []
    
    cmd = [
        "yt-dlp", 
        "--no-playlist"
    ]
    
    # Use Deno for JavaScript runtime
    cmd += ["--js-runtimes", "deno"]
    
    # Add remote components for EJS
    cmd += ["--remote-components", "ejs:npm"]
    
    # Add cookies if they exist
    if os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 100:
        cmd += ["--cookies", COOKIES_PATH]
    
    cmd += [
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--sleep-interval", "2",
        "--max-sleep-interval", "5",
        "--no-check-certificates"
    ]

    cmd += extra_args
    cmd.append(url)
    return cmd

@app.get("/youtube-test")
def youtube_test(url: str):
    extra_args = [
        "--dump-json", 
        "--no-download",
        "--extractor-args", "youtube:player_client=web",
        "--extractor-args", "youtube:po_token=web"
    ]
    cmd = get_yt_dlp_cmd(url, extra_args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Try to parse JSON output if successful
        video_info = None
        if result.returncode == 0 and result.stdout:
            try:
                # Get the first line which should be JSON
                first_line = result.stdout.strip().split('\n')[0]
                video_info = json.loads(first_line)
            except:
                video_info = None
        
        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "video_title": video_info.get('title') if video_info else None,
            "video_id": video_info.get('id') if video_info else None,
            "duration": video_info.get('duration') if video_info else None,
            "channel": video_info.get('channel') if video_info else None,
            "view_count": video_info.get('view_count') if video_info else None,
            "stdout_preview": result.stdout[:500] if result.stdout else "",
            "stderr_preview": result.stderr[:500] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Request timed out after 60 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/youtube-test-simple")
def youtube_test_simple(url: str):
    """Simplest possible test with cookies"""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--cookies", COOKIES_PATH,
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        video_info = None
        if result.returncode == 0 and result.stdout:
            try:
                first_line = result.stdout.strip().split('\n')[0]
                video_info = json.loads(first_line)
            except:
                video_info = None
        
        return {
            "success": result.returncode == 0,
            "video_title": video_info.get('title') if video_info else None,
            "video_id": video_info.get('id') if video_info else None,
            "error": result.stderr[:500] if result.stderr else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
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
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
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
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

@app.get("/ytdlp-version")
def ytdlp_version():
    result = subprocess.run(
        ["yt-dlp", "--version"],
        capture_output=True,
        text=True
    )
    return {
        "version": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

@app.get("/env-check")
def env_check():
    """Check if required executables and cookies are available"""
    executables = ["yt-dlp", "ffmpeg", "node", "deno"]
    results = {}
    
    for exe in executables:
        result = subprocess.run(["which", exe], capture_output=True, text=True)
        results[exe] = {
            "found": result.returncode == 0,
            "path": result.stdout.strip() if result.returncode == 0 else None
        }
    
    # Get yt-dlp version
    version_result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
    results["yt-dlp_version"] = version_result.stdout.strip()
    
    # Check cookies
    results["cookies"] = {
        "exists": os.path.exists(COOKIES_PATH),
        "size": os.path.getsize(COOKIES_PATH) if os.path.exists(COOKIES_PATH) else 0,
        "path": COOKIES_PATH
    }
    
    return results
