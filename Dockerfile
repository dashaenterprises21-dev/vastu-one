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

# STEP 1: Install CPU-only PyTorch FIRST (smaller, ~200 MB instead of 3-4 GB)
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# STEP 2: Install rest of requirements (ultralytics will use existing torch)
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium && playwright install-deps chromium
ENV CHROME_PATH=/usr/bin/chromium
ENV FONT_REGULAR=/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf
ENV FONT_BOLD=/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf
ENV PYTHONUNBUFFERED=1

COPY . .

EXPOSE 8000
CMD ["sh", "-c", "uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-8000}"]
