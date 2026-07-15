import sys
import os

# Tambahkan path root agar modul app terbaca
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.crud import get_fair_route_with_rag

def test():
    db = SessionLocal()
    try:
        print("Menjalankan uji coba fungsi get_fair_route_with_rag...")
        res = get_fair_route_with_rag(db, query="wisata alam", kecamatan="balige")
        print("\nSUKSES!")
        print("Destinasi Utama:", [d.nama for d in res["destinasi_utama"]])
        print("UMKM Sekitar   :", [d.nama for d in res["rekomendasi_umkm_sekitar"]])
    except Exception as e:
        print("\nEROR TERDETEKSI:")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test()
