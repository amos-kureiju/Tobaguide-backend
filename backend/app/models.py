from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Destinasi(Base):
    __tablename__ = "destinasi"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True, nullable=False)
    kategori = Column(String, index=True, nullable=False) # Contoh: 'wisata', 'kuliner', 'umkm', 'akomodasi'
    kecamatan = Column(String, index=True, nullable=False)
    gambar_url = Column(String, nullable=True)
    deskripsi_singkat = Column(Text, nullable=False)
    deskripsi_lengkap = Column(Text, nullable=True)
    nama_jalan = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    jumlah_ulasan = Column(Integer, default=0) # Penting untuk mendeteksi 'hidden gems'