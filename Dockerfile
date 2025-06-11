# 1. Base image
FROM python:3.11-slim

# 2. Install Chrome dependencies
RUN apt-get update && \
    apt-get install -y \
      wget \
      unzip \
      xvfb \
      libxi6 \
      libgconf-2-4 \
      gnupg && \
    rm -rf /var/lib/apt/lists/*

# 3. Download & install Chrome
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i /tmp/chrome.deb || apt-get install -fy && \
    rm /tmp/chrome.deb

# 4. Install matching Chromedriver
RUN CHROME_VER=$(google-chrome --product-version | cut -d'.' -f1-3) && \
    wget -O /tmp/chromedriver.zip \
      "https://chromedriver.storage.googleapis.com/${CHROME_VER}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    rm /tmp/chromedriver.zip

# 5. App code
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 6. Expose & run
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers=1"]
