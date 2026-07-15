import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.crud import create_destinasi
from app.schemas import DestinasiCreate

def main():
    db = SessionLocal()
    try:
        print("Mencoba melakukan insert destinasi secara langsung...")
        payload = DestinasiCreate(
            nama="Destinasi Uji Coba",
            kategori="wisata",
            kecamatan="Balige",
            gambar_url="https://images.unsplash.com/photo-1572252009286-268acec5ca0a",
            deskripsi_singkat="Destinasi uji coba deskripsi singkat",
            deskripsi_lengkap="Deskripsi lengkap uji coba",
            nama_jalan="Jl. Uji Coba",
            latitude=2.33,
            longitude=99.06,
            rating=4.5,
            jumlah_ulasan=5
        )
        res = create_destinasi(db, payload)
        print(f"Sukses! Data dimasukkan dengan ID: {res.id}")
    except Exception as e:
        print("\nEror saat melakukan insert:")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
