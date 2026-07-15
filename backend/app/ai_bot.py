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
    
    # Memanggil model Gemini 3.1 Flash Lite
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt_konteks,
    )
    
    return response.text

def chat_with_bot(user_message: str, history: list) -> str:
    """
    Fungsi untuk ngobrol secara interaktif (Chatbot).
    """
    system_instruction = (
        "Anda adalah TobaRoute AI, asisten pemandu wisata Danau Toba yang ramah, hangat, dan sangat berpengetahuan luas. "
        "Selalu berikan saran yang menonjolkan UMKM lokal dan keadilan pariwisata. Jawab dalam bahasa Indonesia yang natural."
    )
    
    # Konversi history ke format yang diharapkan Gemini (genai.types.Content)
    contents = [{"role": "user", "parts": [{"text": system_instruction}]}]
    
    # Gemini requires alternating roles (user, model). We inject system instruction as user.
    # To keep it simple, we just format the history as a single prompt context.
    
    chat_history_text = system_instruction + "\n\n"
    for msg in history:
        role_name = "Wisatawan" if msg["role"] == "user" else "TobaRoute AI"
        chat_history_text += f"{role_name}: {msg['text']}\n"
    
    chat_history_text += f"Wisatawan: {user_message}\nTobaRoute AI:"
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=chat_history_text,
        )
        return response.text
    except Exception as e:
        print(f"Error in chat_with_bot: {e}")
        return "Mohon maaf, saat ini sistem AI sedang sibuk. Silakan coba beberapa saat lagi."
