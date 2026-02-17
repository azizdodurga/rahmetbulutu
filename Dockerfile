# Python 3.10 kullanıyoruz
FROM python:3.13-slim

# 1. Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 2. Sistem bağımlılıklarını yükle (Postgres ve derleme araçları için şart)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Çalışma dizini
WORKDIR /app

# 4. Önce bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm dosyaları kopyala
COPY . .

# 6. Uygulamayı başlat (PROJE_ADIN kısmını wsgi.py'nin olduğu klasörle değiştir!)
# Örn: klasörün adı 'rahmet' ise 'rahmet.wsgi:application'
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 myproject.wsgi:application