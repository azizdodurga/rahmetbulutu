# Python sürümü
FROM python:3.13-slim

# Gerekli sistem paketlerini yükle (Postgres için)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

# Django'yu Gunicorn ile ayağa kaldır
# ÖNEMLİ: 'your_project_name' kısmını settings.py'nin olduğu klasör adıyla değiştir!
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 myproject.wsgi:application