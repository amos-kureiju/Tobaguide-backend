from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import engine, Base, get_db
from . import crud, schemas

# Otomatis membuat tabel di PostgreSQL saat aplikasi backend dinyalakan
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TobaRoute AI: Backend Keadilan Data")

# Endpoint Baru: Mengambil rekomendasi rute yang adil bagi UMKM berbasis RAG Semantik
@app.get("/api/route/fair-recommendation", response_model=schemas.TobaRouteResponse)
def get_fair_travel_route(query: str, kecamatan: Optional[str] = None, db: Session = Depends(get_db)):
    if not query:
        raise HTTPException(status_code=400, detail="Parameter query (keinginan wisata) harus diisi")
    route_data = crud.get_fair_route_with_rag(db, query=query, kecamatan=kecamatan)
    return route_data

# Endpoint untuk User & Admin: Mengambil daftar destinasi pariwisata
@app.get("/api/destinasi", response_model=List[schemas.DestinasiResponse])
def read_destinasi(kecamatan: str = None, limit: int = 10, db: Session = Depends(get_db)):
    destinasi = crud.get_destinasi(db, kecamatan=kecamatan, limit=limit)
    return destinasi

# Endpoint untuk Admin: Menambahkan destinasi baru ke database
@app.post("/api/admin/destinasi", response_model=schemas.DestinasiResponse)
def add_new_destinasi(destinasi: schemas.DestinasiCreate, db: Session = Depends(get_db)):
    return crud.create_destinasi(db=db, destinasi=destinasi)
