import os
import sys
import pandas as pd
import requests
import json

# Hindari error encoding Unicode pada konsol Windows
sys.stdout.reconfigure(encoding='utf-8')

# 1. Tentukan path file Excel (bisa di folder local atau di folder Downloads)
FILE_PATH = "Dataset HackathonTourism - IT DEL.xlsx"
DOWNLOADS_PATH = r"C:\Users\amosb\Downloads\Dataset HackathonTourism - IT DEL.xlsx"

if os.path.exists(FILE_PATH):
    EXCEL_FILE = FILE_PATH
elif os.path.exists(DOWNLOADS_PATH):
    EXCEL_FILE = DOWNLOADS_PATH
else:
    raise FileNotFoundError("Dataset HackathonTourism - IT DEL.xlsx tidak ditemukan di root maupun folder Downloads.")

# 2. URL Endpoint FastAPI
API_URL = "http://127.0.0.1:8001/api/admin/destinasi"

# Buka file excel untuk membaca sheet-sheetnya
xl = pd.ExcelFile(EXCEL_FILE)
print(f"Berhasil membuka file Excel: {EXCEL_FILE}")
print(f"Sheet yang tersedia: {xl.sheet_names}\n")

# Fungsi pembantu ekstraksi kecamatan
def ekstrak_kecamatan(alamat_teks):
    alamat_lengkap = str(alamat_teks)
    for kec in ["Balige", "Pangururan", "Laguboti", "Muara", "Porsea", "Silaen"]:
        if kec.lower() in alamat_lengkap.lower():
            return kec
    return "Toba"

# ==============================================================================
# FUNGSI 1: INGEST TEMPAT WISATA
# ==============================================================================
def ingest_wisata():
    if "tempat-wisata-v1" not in xl.sheet_names:
        print("Sheet 'tempat-wisata-v1' tidak ditemukan.")
        return
        
    df = pd.read_excel(EXCEL_FILE, sheet_name="tempat-wisata-v1")
    print(f"Memproses Sheet Wisata ({len(df)} baris)...")
    
    for index, row in df.iterrows():
        kecamatan = ekstrak_kecamatan(row.get('add', 'Toba'))
        
        rating_raw = str(row.get('rating', '0.0')).replace(',', '.')
        try:
            rating_clean = float(rating_raw)
        except ValueError:
            rating_clean = 0.0

        deskripsi_gabungan = f"Fasilitas: {row.get('addons', '-')}. Ulasan Awal: {row.get('review', '-')}"
        
        # Koordinat dummy spasial Danau Toba
        latitude = 2.33 + (index * 0.005) 
        longitude = 99.06 + (index * 0.005)

        payload = {
            "nama": str(row.get('place', 'Destinasi Wisata')),
            "kategori": "wisata",
            "kecamatan": kecamatan,
            "gambar_url": str(row.get('gambar_url')) if pd.notna(row.get('gambar_url')) else "https://images.unsplash.com/photo-1572252009286-268acec5ca0a",
            "deskripsi_singkat": f"Destinasi tipe {row.get('type', 'Umum')} dengan tarif masuk {row.get('entry-fee', 'Gratis')}.",
            "deskripsi_lengkap": deskripsi_gabungan,
            "nama_jalan": str(row.get('add', 'Kawasan Danau Toba')),
            "latitude": latitude,
            "longitude": longitude,
            "rating": rating_clean,
            "jumlah_ulasan": 15 + index # Angka ulasan bervariasi
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print(f" [WISATA] Successfully Ingested: {payload['nama']}")
            else:
                print(f"❌ [WISATA] Failed for {payload['nama']}: {response.text}")
        except Exception as e:
            print(f"Error connecting to backend for {payload['nama']}: {e}")

# ==============================================================================
# FUNGSI 2: INGEST KULINER
# ==============================================================================
def ingest_kuliner():
    # Coba gunakan sheet 'kuliner' jika ada, atau fallback ke 'hotel-resto-v1'
    if "kuliner" in xl.sheet_names:
        df = pd.read_excel(EXCEL_FILE, sheet_name="kuliner")
        print(f"\nMemproses Sheet Kuliner ({len(df)} baris)...")
        for index, row in df.iterrows():
            desc = str(row.get('description', 'Makanan khas lokal Danau Toba'))
            kecamatan = ekstrak_kecamatan(desc)
            
            # Simulasi koordinat dan rating rendah ulasan (<15 ulasan, rating > 4.0)
            # Ini sangat krusial untuk melatih algoritma Fairness AI (Keadilan Data) Anda!
            latitude = 2.34 + (index * 0.003)
            longitude = 99.07 + (index * 0.003)
            rating = 4.2 if (index % 2 == 0) else 4.5
            jumlah_ulasan = 5 if (index % 2 == 0) else 8 # Di bawah 15 ulasan

            payload = {
                "nama": str(row.get('kuliner-name', 'Kuliner Lokal')),
                "kategori": "kuliner",
                "kecamatan": kecamatan,
                "gambar_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
                "deskripsi_singkat": desc[:150] + "..." if len(desc) > 150 else desc,
                "deskripsi_lengkap": desc,
                "nama_jalan": f"Sentra Kuliner Kecamatan {kecamatan}",
                "latitude": latitude,
                "longitude": longitude,
                "rating": rating,
                "jumlah_ulasan": jumlah_ulasan
            }
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    print(f" [KULINER] Successfully Ingested: {payload['nama']}")
                else:
                    print(f"❌ [KULINER] Failed for {payload['nama']}: {response.text}")
            except Exception as e:
                print(f"Error: {e}")

    # Tambahan: Ingest data dari hotel-resto-v1 yang berkategori Restoran/Warung
    if "hotel-resto-v1" in xl.sheet_names:
        df_resto = pd.read_excel(EXCEL_FILE, sheet_name="hotel-resto-v1")
        print(f"\nMemproses Sheet Resto dari hotel-resto-v1...")
        for index, row in df_resto.iterrows():
            tipe = str(row.get('type', '')).lower()
            # Hanya ambil yang bertipe kuliner/restoran/cafe
            if 'hotel' not in tipe and 'penginapan' not in tipe:
                kecamatan = ekstrak_kecamatan(row.get('add', 'Toba'))
                rating_raw = str(row.get('rating', '0.0')).replace(',', '.')
                try:
                    rating_clean = float(rating_raw)
                except ValueError:
                    rating_clean = 4.0
                
                # Simulasi ulasan sedikit untuk Fairness test (ulasan < 15)
                jumlah_ulasan = 6 if (index % 2 == 0) else 12

                payload = {
                    "nama": str(row.get('place', 'Resto Lokal')),
                    "kategori": "kuliner",
                    "kecamatan": kecamatan,
                    "gambar_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                    "deskripsi_singkat": f"Tempat kuliner tipe {row.get('type', 'Rumah Makan')} dengan menu khas Danau Toba.",
                    "deskripsi_lengkap": f"Fasilitas: {row.get('facilitates', '-')}. Ulasan: {row.get('review', '-')}",
                    "nama_jalan": str(row.get('add', 'Kawasan Toba')),
                    "latitude": 2.32 + (index * 0.002),
                    "longitude": 99.05 + (index * 0.002),
                    "rating": rating_clean,
                    "jumlah_ulasan": jumlah_ulasan
                }
                try:
                    response = requests.post(API_URL, json=payload)
                    if response.status_code == 200:
                        print(f" [RESTO] Successfully Ingested: {payload['nama']}")
                    else:
                        print(f"❌ [RESTO] Failed for {payload['nama']}: {response.text}")
                except Exception as e:
                    print(f"Error: {e}")

# ==============================================================================
# FUNGSI 3: INGEST TRANSPORTASI (UMKM / Akomodasi Pendukung)
# ==============================================================================
def ingest_transportasi():
    if "transportasi" not in xl.sheet_names:
        print("Sheet 'transportasi' tidak ditemukan.")
        return
        
    df = pd.read_excel(EXCEL_FILE, sheet_name="transportasi")
    print(f"\nMemproses Sheet Transportasi ({len(df)} baris)...")
    
    for index, row in df.iterrows():
        arah = str(row.get('direction', 'Toba'))
        kecamatan = ekstrak_kecamatan(arah)
        
        desc = f"Jenis Mobil: {row.get('jenis-mobil', 'Umum')}. Jam Operasional: {row.get('operational-hour', '-')}. Detail: {row.get('description', '-')}"
        
        # Koordinat dummy
        latitude = 2.35 + (index * 0.004)
        longitude = 99.08 + (index * 0.004)

        payload = {
            "nama": str(row.get('transport-name', 'Transportasi Lokal')),
            "kategori": "umkm", # Kita masukkan ke kategori 'umkm' agar adil bagi pengemudi lokal
            "kecamatan": kecamatan,
            "gambar_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2",
            "deskripsi_singkat": f"Layanan transportasi rute {row.get('direction', 'Lokal')} dengan tarif {row.get('price', '-')}.",
            "deskripsi_lengkap": desc,
            "nama_jalan": f"Terminal / Pool {kecamatan}",
            "latitude": latitude,
            "longitude": longitude,
            "rating": 4.6,
            "jumlah_ulasan": 7 # Ulasan sedikit, potensial masuk Fairness Recommendation!
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print(f" [TRANSPORTASI] Successfully Ingested: {payload['nama']}")
            else:
                print(f"❌ [TRANSPORTASI] Failed for {payload['nama']}: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ingest_wisata()
    ingest_kuliner()
    ingest_transportasi()
    print("\nSemua proses ingestion data selesai!")
