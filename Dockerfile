FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -U yt-dlp

# Tell yt-dlp where node is
RUN echo '[default]\njs-runtimes=node:/usr/bin/node' > /root/.config/yt-dlp/config

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
