import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env using absolute path
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# Fetch the Gemini API key from the environment
api_key = os.getenv("GEMINI_API_KEY")

# Inisialisasi klien dengan API Key yang didapatkan dari .env
client = genai.Client(api_key=api_key)

def generate_tourist_response(user_query: str, fair_route_data: dict) -> str:
    """
    Fungsi untuk menyusun jawaban ramah bagi wisatawan menggunakan arsitektur RAG.
    Menggabungkan pertanyaan user dengan data rute yang sudah disaring adil oleh backend.
    """
    
    # Menyusun prompt instruksi (System Instruction) agar Gemini bertindak sebagai pemandu Toba yang bijak
    prompt_konteks = f"""
    Anda adalah TobaRoute AI, asisten pemandu wisata pintar dan ramah untuk kawasan Danau Toba.
    Wisatawan bertanya: "{user_query}"
    
    Berikut adalah data destinasi dan UMKM lokal terdekat yang sudah disaring secara adil oleh sistem kami:
    {fair_route_data}
    
    Tugas Anda:
    1. Jawab pertanyaan wisatawan dengan gaya bahasa yang ramah, informatif, dan manusiawi.
    2. Rekomendasikan destinasi wisata utama dan sebutkan juga usaha kuliner/UMKM lokal pendukung di sekitarnya agar wisatawan tertarik berkunjung.
    3. Jangan memberikan koordinat secara mentah, cukup sebutkan nama jalan atau kecamatannya saja.
    """
    
    # Memanggil model Gemini 2.0 Flash
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt_konteks,
    )
    
    return response.text
