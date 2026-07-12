# TobaGuide Backend API

A clean, modular FastAPI backend structure for the TobaGuide project.

## Directory Structure

```
tobaguide-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Titik masuk utama aplikasi FastAPI (routes & middleware)
│   ├── config.py        # Konfigurasi database dan environment variables
│   ├── database.py      # Koneksi SQLAlchemy ke PostgreSQL
│   ├── models.py        # Struktur tabel database (SQLAlchemy)
│   ├── schemas.py       # Validasi data masuk/keluar (Pydantic)
│   └── crud.py          # Operasi database (Create, Read, Update, Delete)
├── .env.example             # Template variabel environment
├── .env                     # Variabel environment lokal (jangan dicommit)
├── .gitignore               # Daftar folder & file yang diabaikan Git
└── requirements.txt         # Kebutuhan package Python
```

## Setup & Running Instructions

### 1. Prasyarat (Prerequisites)
Pastikan Anda sudah menginstal Python 3.10+ dan PostgreSQL di sistem Anda.

### 2. Setup Virtual Environment
Buka terminal/command prompt di direktori project `tobaguide-backend` lalu jalankan:

```bash
# Membuat virtual environment
python -m venv venv

# Aktivasi virtual environment (Windows)
venv\Scripts\activate

# Aktivasi virtual environment (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Instal library yang dibutuhkan menggunakan pip:

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
Salin file `.env.example` menjadi `.env` lalu sesuaikan kredensial database PostgreSQL Anda:

```ini
DATABASE_URL="postgresql://postgres:username_db_anda@localhost:5432/nama_db_anda"
```

### 5. Jalankan Aplikasi
Jalankan server pengembangan Uvicorn:

```bash
uvicorn app.main:app --reload
```

Server akan berjalan secara default di `http://127.0.0.1:8000`. 
Anda bisa membuka dokumentasi API interaktif (Swagger UI) di `http://127.0.0.1:8000/docs`.
