FROM python:3.10

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências necessárias (LibreOffice, Chromium, etc.)
RUN apt-get update && apt-get install -y \
    libreoffice \
    wget \
    unzip \
    curl \
    chromium \
    # Instala ChromeDriver 138 manualmente
    && wget https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.92/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver-linux64* \

    fonts-liberation \
    libnss3 \
    libxss1 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Garante que o Chromium esteja no PATH (para Selenium)
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV DISPLAY=:99

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto para o container
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Garante que a config do Streamlit está presente (evita prompt de e-mail)
RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml

# Expõe a porta usada pelo Streamlit
EXPOSE 8501

# Comando para rodar o app Streamlit com as configs adequadas
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
