FROM python:3.10-slim

# 1. Sistem kütüphanelerini yükle (Hata almanı engeller)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Önce bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Kodları kopyala
COPY . .

# 4. ÇALIŞTIRMA KOMUTU (Proje adını değiştirmeyi UNUTMA)
# Örn: klasörün adı 'rahmet' ise 'rahmet.wsgi:application' yaz.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 myproject.wsgi:application