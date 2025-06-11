# 1. Base image with Python
FROM python:3.11-slim

# 2. Install Chrome & deps
RUN apt-get update && \
    apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 \
    && wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
       | dpkg -i - && apt-get install -fy && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 3. Install matching Chromedriver
RUN CHROME_VER=$(google-chrome --product-version | cut -d'.' -f1-3) && \
    wget -O /tmp/chromedriver.zip \
      "https://chromedriver.storage.googleapis.com/${CHROME_VER}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    rm /tmp/chromedriver.zip

# 4. App setup
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5. Expose and run
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers=1"]