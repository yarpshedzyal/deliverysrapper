# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to avoid prompts during installations
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome version 114
RUN wget -O /tmp/google-chrome-stable_114.0.5735.198-1_amd64.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    apt-get update && apt-get install -y /tmp/google-chrome-stable_114.0.5735.198-1_amd64.deb && \
    rm /tmp/google-chrome-stable_114.0.5735.198-1_amd64.deb

# Download ChromeDriver version 114
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set display port as an environment variable
ENV DISPLAY=:99

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD ["python", "bot.py"]
