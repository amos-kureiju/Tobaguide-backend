import React, { useState } from 'react';
import { Search, Map, Sparkles, AlertCircle, Compass } from 'lucide-react';
import { getFairRecommendation } from './services/api';
import DestinationCard from './components/DestinationCard';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [kecamatan, setKecamatan] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) {
      setError('Mohon masukkan keinginan wisata Anda (misal: "tempat yang tenang dan sejuk")');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const data = await getFairRecommendation(query, kecamatan);
      setResults(data);
    } catch (err) {
      setError('Gagal mengambil rekomendasi. Pastikan backend TobaGuide berjalan (localhost:8080).');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Navbar */}
      <nav className="navbar glass-panel">
        <div className="container nav-content">
          <div className="logo">
            <Compass size={28} color="var(--color-primary)" />
            <h1>TobaRoute <span className="highlight">AI</span></h1>
          </div>
          <div className="nav-links">
            <a href="#" className="active">Beranda</a>
            <a href="#">Jelajah</a>
            <a href="#">Tentang</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="hero">
        <div className="hero-background"></div>
        <div className="container hero-content fade-in">
          <h2>Temukan Keindahan Danau Toba</h2>
          <p>Asisten AI kami akan merancang rute perjalanan yang adil, merekomendasikan destinasi populer sekaligus memajukan UMKM lokal.</p>
          
          <form className="search-form glass-panel" onSubmit={handleSearch}>
            <div className="input-group">
              <Search className="input-icon" size={20} />
              <input 
                type="text" 
                placeholder="Apa yang ingin Anda lakukan? (e.g. Tempat bersejarah untuk keluarga)" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
            <div className="input-group location">
              <Map className="input-icon" size={20} />
              <select value={kecamatan} onChange={(e) => setKecamatan(e.target.value)}>
                <option value="">Semua Kecamatan</option>
                <option value="Balige">Balige</option>
                <option value="Porsea">Porsea</option>
                <option value="Lumban Julu">Lumban Julu</option>
                <option value="Tampahan">Tampahan</option>
                <option value="Pangururan">Pangururan</option>
                <option value="Simanindo">Simanindo</option>
                <option value="Harian">Harian</option>
                <option value="Muara">Muara</option>
              </select>
            </div>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? (
                <div className="spinner"></div>
              ) : (
                <>
                  <Sparkles size={18} />
                  Cari Rute
                </>
              )}
            </button>
          </form>
          {error && (
            <div className="error-message fade-in">
              <AlertCircle size={18} /> {error}
            </div>
          )}
        </div>
      </header>

      {/* Results Section */}
      <main className="container main-content">
        {loading && (
          <div className="loading-state">
            <div className="skeleton-loading ai-bubble-skeleton"></div>
            <div className="grid">
              <div className="skeleton-loading card-skeleton"></div>
              <div className="skeleton-loading card-skeleton"></div>
              <div className="skeleton-loading card-skeleton"></div>
            </div>
          </div>
        )}

        {results && !loading && (
          <div className="results-container fade-in">
            {/* AI Response */}
            <section className="ai-response glass-panel">
              <div className="ai-header">
                <Sparkles size={24} color="var(--color-primary)" />
                <h3>Saran Perjalanan dari AI</h3>
              </div>
              <div className="ai-body">
                <ReactMarkdown>{results.ai_response}</ReactMarkdown>
              </div>
            </section>

            {/* Destinations */}
            <section className="destinations-section">
              <div className="section-header">
                <h2>Destinasi Utama</h2>
                <div className="line"></div>
              </div>
              {results.destinasi_utama.length > 0 ? (
                <div className="grid">
                  {results.destinasi_utama.map(dest => (
                    <DestinationCard key={dest.id} dest={dest} isUmkm={false} />
                  ))}
                </div>
              ) : (
                <p className="no-data">Tidak ada destinasi utama yang ditemukan untuk pencarian ini.</p>
              )}
            </section>

            {/* UMKM */}
            <section className="umkm-section">
              <div className="section-header">
                <h2>Dukung UMKM Lokal Sekitar</h2>
                <div className="line line-accent"></div>
              </div>
              {results.rekomendasi_umkm_sekitar.length > 0 ? (
                <div className="grid">
                  {results.rekomendasi_umkm_sekitar.map(umkm => (
                    <DestinationCard key={umkm.id} dest={umkm} isUmkm={true} />
                  ))}
                </div>
              ) : (
                <p className="no-data">Tidak ada rekomendasi UMKM untuk pencarian ini.</p>
              )}
            </section>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>&copy; 2026 TobaRoute AI. Dibangun untuk mendukung Keadilan Pariwisata Danau Toba.</p>
      </footer>
    </div>
  );
}

export default App;
