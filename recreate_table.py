import os
import sys

# Tambahkan path root agar modul app terbaca
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database import engine, Base
from app.models import Destinasi

def main():
    print("Menghubungkan ke database...")
    print("Menghapus tabel 'destinasi' lama (drop)...")
    Destinasi.__table__.drop(bind=engine, checkfirst=True)
    
    print("Membuat kembali tabel 'destinasi' dengan kolom baru (kategori & jumlah_ulasan)...")
    Base.metadata.create_all(bind=engine)
    print("Tabel berhasil diperbarui!")

if __name__ == "__main__":
    main()
