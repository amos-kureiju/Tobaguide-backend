# TobaRoute AI Monorepo

Repositori ini menggabungkan sistem backend (FastAPI) dan frontend (React + Vite) untuk aplikasi panduan pariwisata Danau Toba yang adil bagi UMKM berbasis RAG Semantik.

## 📂 Struktur Proyek
- `/backend`: Berisi logika backend FastAPI, model database, skrip ingestion, dan virtual environment.
- `/frontend`: Berisi antarmuka pengguna berbasis React, Vite, dan Vanilla CSS.

---

## 🛠️ Cara Memasang & Menjalankan di Laptop Anda

### Langkah 1: Kloning Repositori
Jika Anda baru pertama kali mengambil proyek ini, kloning repositori ini ke komputer Anda:
```bash
git clone https://github.com/amos-kureiju/Tobaguide-backend.git tobaguide
cd tobaguide
```

---

### Langkah 2: Setup Backend (FastAPI)

1. Pindah ke direktori backend:
   ```bash
   cd backend
   ```

2. Buat Virtual Environment baru:
   ```bash
   python -m venv venv
   ```

3. Aktifkan Virtual Environment:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Pasang Dependensi Python:
   ```bash
   pip install -r requirements.txt
   pip install pinecone-client cohere openai pandas openpyxl
   ```

5. Konfigurasi file `.env`:
   Salin file `.env.example` menjadi `.env` lalu lengkapi isinya (seperti Database URL, API Keys Gemini, Cohere, Pinecone, dll.):
   ```bash
   copy .env.example .env
   ```

6. Jalankan Server Backend:
   ```bash
   uvicorn app.main:app --port 8080 --reload
   ```
   *Backend akan berjalan di: `http://localhost:8080`*

---

### Langkah 3: Setup Frontend (React + Vite)

1. Buka terminal baru dan masuk ke direktori frontend:
   ```bash
   cd frontend
   ```

2. Pasang Dependensi Node.js:
   ```bash
   npm install
   ```

3. Jalankan Server Frontend:
   ```bash
   npm run dev
   ```
   *Frontend akan berjalan di: `http://localhost:5173`*

---

### 🌐 Akses Aplikasi:
Buka browser Anda dan buka alamat:
- **Web App:** [http://localhost:5173](http://localhost:5173)
- **API Docs (Swagger UI):** [http://localhost:8080/docs](http://localhost:8080/docs)
