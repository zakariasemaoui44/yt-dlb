FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install yt-dlp via pip
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Update yt-dlp to latest version and set up EJS
RUN pip install -U yt-dlp

# Download the EJS script that yt-dlp needs for YouTube n-challenge
RUN yt-dlp --install-to-path /usr/local/bin --update-to nightly || true
RUN mkdir -p /root/.config/yt-dlp

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
