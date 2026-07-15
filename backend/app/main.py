from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import engine, Base, get_db
from . import crud, schemas
from .ai_bot import generate_tourist_response

# Otomatis membuat tabel di PostgreSQL saat aplikasi backend dinyalakan
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TobaRoute AI: Backend Keadilan Data")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint Baru: Mengambil rekomendasi rute yang adil bagi UMKM berbasis RAG Semantik
@app.get("/api/route/fair-recommendation", response_model=schemas.TobaRouteResponse)
def get_fair_travel_route(query: str, kecamatan: Optional[str] = None, db: Session = Depends(get_db)):
    print(f"\n[DIAGNOSTIC] Endpoint /api/route/fair-recommendation dipanggil dengan query: {query}, kecamatan: {kecamatan}")
    if not query:
        raise HTTPException(status_code=400, detail="Parameter query (keinginan wisata) harus diisi")
    
    # 1. Ambil data rute terstruktur (destinasi utama & UMKM sekitar)
    route_data = crud.get_fair_route_with_rag(db, query=query, kecamatan=kecamatan)
    
    # 2. Hasilkan panduan wisata AI berbasis RAG menggunakan Gemini API secara aman
    try:
        ai_response = generate_tourist_response(user_query=query, fair_route_data=route_data)
    except Exception as e:
        print(f"[AI Error] Gagal menghubungi Gemini API: {e}")
        ai_response = "[INFO] Asisten AI TobaRoute sedang sibuk atau batas kuota terlampaui. Menampilkan rekomendasi destinasi terdekat langsung dari database."
    
    return {
        "destinasi_utama": route_data["destinasi_utama"],
        "rekomendasi_umkm_sekitar": route_data["rekomendasi_umkm_sekitar"],
        "ai_response": ai_response
    }

# Endpoint untuk User & Admin: Mengambil daftar destinasi pariwisata
@app.get("/api/destinasi", response_model=List[schemas.DestinasiResponse])
def read_destinasi(kecamatan: str = None, limit: int = 10, db: Session = Depends(get_db)):
    destinasi = crud.get_destinasi(db, kecamatan=kecamatan, limit=limit)
    return destinasi

# Endpoint untuk Admin: Menambahkan destinasi baru ke database
@app.post("/api/admin/destinasi", response_model=schemas.DestinasiResponse)
def add_new_destinasi(destinasi: schemas.DestinasiCreate, db: Session = Depends(get_db)):
    return crud.create_destinasi(db=db, destinasi=destinasi)
