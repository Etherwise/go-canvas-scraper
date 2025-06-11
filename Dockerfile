# 1) Use the infologistix selenium-python image (has Chrome + Chromedriver + Python 3.10)
FROM infologistix/docker-selenium-python:3.10

# 2) Switch to your app dir
WORKDIR /app

# 3) Copy only requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy your code
COPY . .

# 5) Expose port & launch via Gunicorn
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers=1"]
