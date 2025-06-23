# Use a lightweight Python image
FROM python:3.10-slim

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install LibreOffice and required system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    ttf-mscorefonts-installer \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Chromium to PATH for Selenium
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV DISPLAY=:99

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
