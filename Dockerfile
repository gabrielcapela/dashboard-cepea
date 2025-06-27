FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

# Instala LibreOffice e Chromium com dependências essenciais
RUN apt-get update && apt-get install -y \
    libreoffice \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Garante que o Chromium esteja no PATH para o Selenium
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV DISPLAY=:99

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
