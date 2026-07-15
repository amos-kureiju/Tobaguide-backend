from pydantic import BaseModel
from typing import Optional, List

# Base schema untuk struktur data destinasi
class DestinasiBase(BaseModel):
    nama: str
    kategori: str
    kecamatan: str
    gambar_url: Optional[str] = None
    deskripsi_singkat: str
    deskripsi_lengkap: Optional[str] = None
    nama_jalan: str
    latitude: float
    longitude: float
    rating: float
    jumlah_ulasan: int = 0

# Digunakan saat Admin menginput data baru (Data masuk)
class DestinasiCreate(DestinasiBase):
    pass

# Digunakan saat API merespons permintaan User/Admin (Data keluar)
class DestinasiResponse(DestinasiBase):
    id: int

    class Config:
        from_attributes = True

# Skema permintaan untuk AI Chatbot
class ChatRequest(BaseModel):
    user_query: str
    fair_route_data: dict


# Skema khusus untuk merespons rute pintar yang adil
class TobaRouteResponse(BaseModel):
    destinasi_utama: List[DestinasiResponse]
    rekomendasi_umkm_sekitar: List[DestinasiResponse]
    ai_response: Optional[str] = None

class ChatbotMessage(BaseModel):
    role: str
    text: str

class ChatbotRequest(BaseModel):
    message: str
    history: List[ChatbotMessage] = []
