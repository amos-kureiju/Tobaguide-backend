from sqlalchemy.orm import Session
from . import models, schemas
import math

# Menampilkan semua destinasi (Bisa difilter berdasarkan kecamatan untuk kebutuhan User/Admin)
def get_destinasi(db: Session, kecamatan: str = None, limit: int = 10):
    query = db.query(models.Destinasi)
    if kecamatan:
        query = query.filter(models.Destinasi.kecamatan.ilike(kecamatan))
    return query.order_by(models.Destinasi.rating.desc()).limit(limit).all()

# Fungsi untuk Admin menambah destinasi baru
def create_destinasi(db: Session, destinasi: schemas.DestinasiCreate):
    db_destinasi = models.Destinasi(**destinasi.model_dump())
    db.add(db_destinasi)
    db.commit()
    db.refresh(db_destinasi)
    return db_destinasi

# Fungsi bantuan untuk menghitung jarak koordinat (Haversine Formula) jika diperlukan di lokal
def hitung_jarak(lat1, lon1, lat2, lon2):
    rad = math.pi / 180
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad
    a = math.sin(dlat/2)**2 + math.cos(lat1*rad) * math.cos(lat2*rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371 * c # Jarak dalam Kilometer

def get_fair_route(db: Session, kecamatan: str, limit_utama: int = 3):
    # 1. Ambil destinasi wisata utama dengan rating tertinggi di kecamatan tersebut
    destinasi_utama = db.query(models.Destinasi).\
        filter(models.Destinasi.kecamatan.ilike(kecamatan)).\
        filter(models.Destinasi.kategori == 'wisata').\
        order_by(models.Destinasi.rating.desc()).\
        limit(limit_utama).all()
    
    # 2. Ambil pendukung UMKM/Kuliner lokal yang terkena bias (ulasan sedikit) sebagai bentuk keadilan data
    # Kriteria: ulasan di bawah 15 tapi rating di atas 4.0
    umkm_sekitar = db.query(models.Destinasi).\
        filter(models.Destinasi.kecamatan.ilike(kecamatan)).\
        filter(models.Destinasi.kategori.in_(['umkm', 'kuliner'])).\
        filter(models.Destinasi.jumlah_ulasan < 15).\
        filter(models.Destinasi.rating >= 4.0).\
        order_by(models.Destinasi.rating.desc()).\
        limit(4).all()
        
    return {
        "destinasi_utama": destinasi_utama,
        "rekomendasi_umkm_sekitar": umkm_sekitar
    }

# ==============================================================================
# INTEGRASI RAG & VECTOR DATABASE (PINECONE)
# ==============================================================================
from pinecone import Pinecone
from openai import OpenAI
from app.config import settings

def get_pinecone_index():
    if settings.PINECONE_API_KEY and settings.PINECONE_INDEX_NAME:
        try:
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            return pc.Index(settings.PINECONE_INDEX_NAME)
        except Exception as e:
            print(f"[RAG] Gagal inisialisasi Pinecone: {e}")
    return None

def get_cohere_embedding(query_user: str):
    try:
        from cohere import Client
        co = Client(api_key=settings.COHERE_API_KEY)
        res = co.embed(texts=[query_user], model="embed-multilingual-v3.0", input_type="search_query")
        return res.embeddings[0]
    except Exception as e:
        print(f"[RAG] Cohere Embedding failed: {e}")
        return [0.1] * 1024 # Dummy fallback

def cari_destinasi_semantik(query_user: str, top_k: int = 20):
    query_vector = None
    
    # Pilih model embedding yang tersedia (OpenAI atau Cohere fallback)
    if settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("sk-proj-placeholder"):
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.embeddings.create(
                input=[query_user],
                model="text-embedding-3-small"
            )
            query_vector = response.data[0].embedding
        except Exception as e:
            print(f"[RAG] OpenAI Embedding failed: {e}. Falling back to Cohere...")
            query_vector = get_cohere_embedding(query_user)
    else:
        query_vector = get_cohere_embedding(query_user)

    # Lakukan pencarian di Pinecone
    index = get_pinecone_index()
    if index and query_vector:
        try:
            results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
            return [match.id for match in results.matches]
        except Exception as e:
            print(f"[RAG] Pinecone Query failed: {e}")
    return []

def get_fair_route_with_rag(db: Session, query: str, kecamatan: str = None, limit_utama: int = 3):
    # 1. Cari ID destinasi yang paling cocok secara makna lewat Pinecone
    matched_ids = cari_destinasi_semantik(query)
    
    # 2. Ambil destinasi wisata utama dari PostgreSQL
    query_wisata = db.query(models.Destinasi).filter(models.Destinasi.kategori == 'wisata')
    if kecamatan:
        query_wisata = query_wisata.filter(models.Destinasi.kecamatan.ilike(kecamatan))
        
    if matched_ids:
        # Konversi ke int id karena id di Postgres bertipe Integer
        int_ids = []
        for mid in matched_ids:
            try:
                int_ids.append(int(mid))
            except ValueError:
                pass
        
        if int_ids:
            # Ambil destinasi yang ada di matched_ids
            destinasi_utama = query_wisata.filter(models.Destinasi.id.in_(int_ids)).all()
            # Urutkan berdasarkan kemiripan dari Pinecone
            id_to_dest = {d.id: d for d in destinasi_utama}
            destinasi_utama = [id_to_dest[id_] for id_ in int_ids if id_ in id_to_dest][:limit_utama]
        else:
            destinasi_utama = query_wisata.order_by(models.Destinasi.rating.desc()).limit(limit_utama).all()
    else:
        # Fallback pencarian terpopuler biasa
        destinasi_utama = query_wisata.order_by(models.Destinasi.rating.desc()).limit(limit_utama).all()

    # 3. Ambil pendukung UMKM/Kuliner lokal terdekat (Keadilan Data / Fairness)
    target_kecamatans = list(set([d.kecamatan for d in destinasi_utama]))
    if not target_kecamatans and kecamatan:
        target_kecamatans = [kecamatan]
        
    umkm_query = db.query(models.Destinasi).filter(models.Destinasi.kategori.in_(['umkm', 'kuliner']))
    if target_kecamatans:
        umkm_query = umkm_query.filter(models.Destinasi.kecamatan.in_(target_kecamatans))
        
    umkm_sekitar = umkm_query.filter(models.Destinasi.jumlah_ulasan < 15).\
        filter(models.Destinasi.rating >= 4.0).\
        order_by(models.Destinasi.rating.desc()).\
        limit(4).all()
        
    return {
        "destinasi_utama": destinasi_utama,
        "rekomendasi_umkm_sekitar": umkm_sekitar
    }
