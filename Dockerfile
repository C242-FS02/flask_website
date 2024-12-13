# Gunakan image base Python 3.9 slim
FROM python:3.9-slim

# Set working directory di container
WORKDIR /app

# Install dependencies sistem yang diperlukan
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    gnupg \
    curl \
    libexpat1 \
    && rm -rf /var/lib/apt/lists/*

# Buat direktori yang diperlukan
RUN mkdir -p ./models/ \
    ./static/images/ \
    ./static/png/ \
    ./static/results/

# Unduh model file langsung ke folder `models/`
RUN curl -o ./models/sam_vit_b_01ec64.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth

# Copy file requirements terlebih dahulu agar proses build memanfaatkan cache Docker
COPY requirements.txt ./

# Install library Python dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua kode aplikasi ke container
COPY . .

# Expose port default Flask (5000)
EXPOSE 5000

# Jalankan aplikasi menggunakan Gunicorn untuk performa yang lebih baik
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
