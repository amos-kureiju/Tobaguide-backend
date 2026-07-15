import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Menemukan path absolut ke file .env di folder root (satu tingkat di atas folder 'app')
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"

# Memuat file .env menggunakan path absolut dan memaksa override sistem
load_dotenv(dotenv_path=dotenv_path, override=True)

# Mengambil DATABASE_URL dari .env, default jika tidak ditemukan
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/tobaguide_db"
)

print(f"[DIAGNOSTIC] DATABASE URL: {SQLALCHEMY_DATABASE_URL}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Fungsi untuk mendapatkan sesi database di setiap request API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()