FROM python:3.10

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Chromium and essential dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    wget \
    unzip \
    curl \
    chromium \
    fonts-liberation \
    libnss3 \
    libxss1 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Chromium is in the PATH
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV DISPLAY=:99

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Streamlit configuration folder
COPY .streamlit /app/.streamlit

# Expose Streamlit's default port
EXPOSE 8501

# Define the command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
