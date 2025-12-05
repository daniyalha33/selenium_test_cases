# Use official Python image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl xvfb gnupg libnss3 libxss1 libasound2 fonts-liberation libgtk-3-0 libx11-xcb1 && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set working directory
WORKDIR /tests

# Copy test requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy test code
COPY . .

# Set entrypoint to pytest
ENTRYPOINT ["pytest", "--headless", "--maxfail=1", "--disable-warnings"]
