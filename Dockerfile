FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    fonts-noto \
    fonts-noto-cjk \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium && playwright install-deps chromium

COPY . .

ENV CHROME_PATH=/usr/bin/chromium
ENV FONT_REGULAR=/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf
ENV FONT_BOLD=/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["sh", "-c", "uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-8000}"]
