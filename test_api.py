import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("=== PENGUJIAN API TOBAGUIDE-BACKEND ===")
    
    # 1. Cek kesehatan server (Health Check via /docs)
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("[OK] Server FastAPI aktif!")
        else:
            print(f"[FAIL] Server mengembalikan status {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("[FAIL] Server Uvicorn belum dijalankan! Jalankan '.\\venv\\Scripts\\uvicorn app.main:app --reload' terlebih dahulu.")
        return

    # 2. Tambah data destinasi baru (Admin POST)
    print("\n1. Mengirim data destinasi baru (POST /api/admin/destinasi)...")
    payload = {
        "nama": "Pantai Bulbul Balige",
        "kategori": "Wisata Alam",
        "kecamatan": "Balige",
        "gambar_url": "https://example.com/pantai-bulbul.jpg",
        "deskripsi_singkat": "Pantai berpasir putih yang indah di pinggiran Danau Toba.",
        "deskripsi_lengkap": "Pantai Bulbul terletak di Balige, Toba. Sangat cocok untuk keluarga dengan fasilitas permainan air dan dekat dengan warung kuliner tradisional.",
        "nama_jalan": "Jl. Bulbul, Lumban Bulbul",
        "latitude": 2.3456,
        "longitude": 99.0678,
        "rating": 4.8,
        "jumlah_ulasan": 120
    }
    
    post_resp = requests.post(f"{BASE_URL}/api/admin/destinasi", json=payload)
    if post_resp.status_code == 200:
        print(f"[OK] Destinasi berhasil ditambahkan! ID: {post_resp.json().get('id')}")
    else:
        print(f"[FAIL] Gagal menambah destinasi: {post_resp.text}")

    # 3. Ambil data destinasi (GET /api/destinasi)
    print("\n2. Mengambil daftar destinasi (GET /api/destinasi)...")
    get_resp = requests.get(f"{BASE_URL}/api/destinasi?kecamatan=Balige")
    if get_resp.status_code == 200:
        destinasis = get_resp.json()
        print(f"[OK] Ditemukan {len(destinasis)} destinasi di Balige:")
        for d in destinasis:
            print(f"   - {d['nama']} ({d['nama_jalan']}) - Rating: {d['rating']}")
    else:
        print(f"[FAIL] Gagal mengambil destinasi: {get_resp.text}")

    # 4. Tes Rekomendasi RAG AI (GET /api/route/fair-recommendation)
    print("\n3. Menguji Rekomendasi Pintar AI (GET /api/route/fair-recommendation)...")
    route_resp = requests.get(f"{BASE_URL}/api/route/fair-recommendation", params={
        "query": "Saya mau ke pantai di Balige lalu makan di dekatnya",
        "kecamatan": "Balige"
    })
    
    if route_resp.status_code == 200:
        data = route_resp.json()
        print("[OK] Respon Rute & Gemini AI berhasil diterima!")
        print("\n--- Rekomendasi AI Pemandu Wisata ---")
        print(data.get("ai_response"))
        print("--------------------------------------")
    else:
        print(f"[FAIL] Gagal mengambil rekomendasi AI: {route_resp.text}")

if __name__ == "__main__":
    test_api()
