import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Tambahkan path proyek agar modul app terbaca
sys.path.append(str(BASE_DIR))

from app.database import SessionLocal
from app import models

# Import AI Clients
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
try:
    from cohere import Client as CohereClient
except ImportError:
    CohereClient = None

# Konfigurasi dari Environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tobaguide-index")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def get_embedding_model_info():
    """Menentukan model embedding dan dimensi berdasarkan API key yang tersedia"""
    if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-placeholder"):
        return "openai", "text-embedding-3-small", 1536
    elif COHERE_API_KEY and not COHERE_API_KEY.startswith("cohere-placeholder"):
        return "cohere", "embed-multilingual-v3.0", 1024
    else:
        print("[ERROR] Tidak ditemukan API Key OpenAI atau Cohere yang valid di file .env")
        sys.exit(1)

def generate_embeddings_batch(provider, model_name, texts, openai_client, cohere_client):
    """Menghasilkan vektor embedding untuk satu batch teks masukan"""
    if provider == "openai":
        response = openai_client.embeddings.create(
            input=texts,
            model=model_name
        )
        return [item.embedding for item in response.data]
    elif provider == "cohere":
        response = cohere_client.embed(
            texts=texts,
            model=model_name,
            input_type="search_document"
        )
        return response.embeddings
    return []

def main():
    print("=== SINKRONISASI DATA TOBAGUIDE KE PINECONE ===")
    
    # 1. Validasi API Key Pinecone
    if not PINECONE_API_KEY:
        print("[ERROR] PINECONE_API_KEY tidak ditemukan di .env")
        sys.exit(1)
        
    provider, model_name, dimension = get_embedding_model_info()
    print(f"[INFO] Provider Embedding: {provider.upper()} ({model_name}) | Dimensi Vektor: {dimension}")
    
    # 2. Inisialisasi AI Clients
    openai_client = OpenAI(api_key=OPENAI_API_KEY) if provider == "openai" else None
    cohere_client = CohereClient(api_key=COHERE_API_KEY) if provider == "cohere" else None
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # 3. Validasi & Buat Indeks Pinecone Jika Belum Ada
    print(f"Checking index '{PINECONE_INDEX_NAME}' di Pinecone...")
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"[INFO] Indeks '{PINECONE_INDEX_NAME}' tidak ditemukan. Membuat indeks baru...")
        try:
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print(f"[OK] Indeks '{PINECONE_INDEX_NAME}' berhasil dibuat! Menunggu inisialisasi...")
            # Menunggu beberapa detik agar indeks aktif
            time.sleep(8)
        except Exception as e:
            print(f"[ERROR] Gagal membuat indeks Pinecone: {e}")
            sys.exit(1)
    else:
        print(f"[OK] Indeks '{PINECONE_INDEX_NAME}' terdeteksi dan aktif.")
        
    index = pc.Index(PINECONE_INDEX_NAME)
    
    # 4. Ambil Data Destinasi dari PostgreSQL
    db = SessionLocal()
    try:
        destinasis = db.query(models.Destinasi).all()
        print(f"Menarik {len(destinasis)} destinasi dari PostgreSQL...")
        
        if not destinasis:
            print("[WARN] Database kosong. Silakan jalankan 'ingest_data.py' terlebih dahulu.")
            return
            
        # 5. Proses Embedding dalam Batch
        vectors_to_upsert = []
        batch_embedding_size = 90  # Ukuran batch untuk API call Cohere/OpenAI (Max 96)
        
        print("\nMulai menghasilkan embedding secara berkelompok...")
        for idx in range(0, len(destinasis), batch_embedding_size):
            batch_items = destinasis[idx:idx + batch_embedding_size]
            batch_texts = []
            
            for d in batch_items:
                semantik_text = (
                    f"Nama: {d.nama} | "
                    f"Kategori: {d.kategori} | "
                    f"Kecamatan: {d.kecamatan} | "
                    f"Deskripsi: {d.deskripsi_singkat} {d.deskripsi_lengkap or ''} | "
                    f"Jalan: {d.nama_jalan}"
                )
                batch_texts.append(semantik_text)
            
            try:
                # Panggil API sekali saja untuk seluruh batch
                embeddings = generate_embeddings_batch(provider, model_name, batch_texts, openai_client, cohere_client)
                
                # Petakan kembali vektor ke objek destinasi
                for item, vector_values in zip(batch_items, embeddings):
                    vectors_to_upsert.append({
                        "id": str(item.id),
                        "values": vector_values,
                        "metadata": {
                            "nama": item.nama,
                            "kategori": item.kategori,
                            "kecamatan": item.kecamatan,
                            "deskripsi_singkat": item.deskripsi_singkat,
                            "nama_jalan": item.nama_jalan
                        }
                    })
                
                print(f" -> Berhasil membuat embedding batch: {len(vectors_to_upsert)} / {len(destinasis)} data.")
                
                # Jeda sejenak untuk mematuhi rate limit rate API trial key
                time.sleep(2)
                
            except Exception as e:
                print(f"[ERROR] Gagal memproses batch dari index {idx} ke {idx + len(batch_items)}: {e}")
                
        # 6. Unggah dalam Batch ke Pinecone
        if vectors_to_upsert:
            print(f"\nMengunggah {len(vectors_to_upsert)} vektor ke Pinecone...")
            # Bagi menjadi batch-batch kecil berukuran 50 vektor untuk upsert Pinecone
            pinecone_batch_size = 50
            for i in range(0, len(vectors_to_upsert), pinecone_batch_size):
                batch = vectors_to_upsert[i:i + pinecone_batch_size]
                index.upsert(vectors=batch)
                print(f" [OK] Berhasil mengunggah batch {i//pinecone_batch_size + 1} ({len(batch)} data)")
            
            print("\n[SUCCESS] Sinkronisasi seluruh data ke Pinecone berhasil diselesaikan!")
        else:
            print("[WARN] Tidak ada vektor yang siap diunggah.")
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
