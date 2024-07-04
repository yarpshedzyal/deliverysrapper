# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set ChromeDriver version
ENV CHROMEDRIVER_VERSION=114.0.5735.90
ENV CHROMIUM_VERSION=114.0.5735.90

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libu2f-udev \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chromium
RUN wget -q -O /tmp/chromium.deb "https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/$CHROMIUM_VERSION/chrome-linux.zip" \
    && unzip /tmp/chromium.deb -d /opt/chromium/ \
    && ln -s /opt/chromium/chrome-linux/chrome /usr/bin/chromium \
    && rm /tmp/chromium.deb

# Download and install ChromeDriver
RUN wget -q -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Set the path for ChromeDriver
ENV PATH=/usr/local/bin/chromedriver:$PATH

# Verify Chromium installation
RUN chromium --version && chromedriver --version

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Define the command to run your application
CMD ["python", "bot.py"]
