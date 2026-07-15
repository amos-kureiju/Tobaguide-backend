import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { getDestinations } from '../services/api';
import { Map, AlertCircle, Navigation, Star, Info } from 'lucide-react';

// Custom icons using external URLs to avoid Vite asset resolution issues with Leaflet
const wisataIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const umkmIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const Explore = () => {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Center map to Danau Toba coordinates
  const TOBA_CENTER = [2.6105, 98.8106];

  useEffect(() => {
    const fetchAllDestinations = async () => {
      try {
        setLoading(true);
        // Fetch up to 200 destinations for the map
        const data = await getDestinations('', 200);
        setDestinations(data);
      } catch (err) {
        console.error(err);
        setError('Gagal memuat data lokasi dari server.');
      } finally {
        setLoading(false);
      }
    };

    fetchAllDestinations();
  }, []);

  return (
    <main className="container main-content fade-in" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="explore-header" style={{ marginBottom: '2rem' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-primary-dark)' }}>
          <Map size={32} /> Peta Sebaran Wisata & UMKM
        </h1>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '1.1rem', marginTop: '0.5rem' }}>
          Jelajahi keindahan Danau Toba. Pin biru adalah lokasi wisata utama, dan pin hijau adalah lokasi UMKM lokal.
        </p>
      </div>

      {error && (
        <div className="error-message fade-in" style={{ marginBottom: '1rem' }}>
          <AlertCircle size={18} /> {error}
        </div>
      )}

      {loading ? (
        <div className="loading-state" style={{ height: '500px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="spinner" style={{ borderColor: 'var(--color-primary)', borderTopColor: 'transparent', width: '40px', height: '40px' }}></div>
        </div>
      ) : (
        <div className="map-container-wrapper glass-panel" style={{ height: '600px', width: '100%', borderRadius: 'var(--radius-lg)', overflow: 'hidden', padding: '0.5rem' }}>
          <MapContainer 
            center={TOBA_CENTER} 
            zoom={10} 
            style={{ height: '100%', width: '100%', borderRadius: 'calc(var(--radius-lg) - 0.5rem)' }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {destinations.map(dest => {
              const isUmkm = dest.kategori.toLowerCase() === 'umkm';
              
              // Cek apakah punya latitude longitude yang valid
              if (!dest.latitude || !dest.longitude) return null;

              return (
                <Marker 
                  key={dest.id} 
                  position={[dest.latitude, dest.longitude]} 
                  icon={isUmkm ? umkmIcon : wisataIcon}
                >
                  <Popup>
                    <div style={{ minWidth: '200px' }}>
                      <h4 style={{ margin: '0 0 0.5rem 0', color: isUmkm ? 'var(--color-accent-dark, #16a34a)' : 'var(--color-primary-dark)' }}>
                        {dest.nama}
                      </h4>
                      
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.5rem', fontSize: '0.85rem', color: '#64748b' }}>
                        <Navigation size={12} /> {dest.kecamatan}
                      </div>
                      
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.75rem', fontSize: '0.85rem', color: '#64748b' }}>
                        <Star size={12} fill="#fbbf24" color="#fbbf24" /> {dest.rating} ({dest.jumlah_ulasan})
                      </div>

                      <p style={{ margin: '0', fontSize: '0.9rem', lineHeight: '1.4' }}>
                        {dest.deskripsi_singkat}
                      </p>
                      
                      {isUmkm && (
                        <div style={{ marginTop: '0.75rem', padding: '0.25rem 0.5rem', background: '#dcfce7', color: '#166534', borderRadius: '4px', fontSize: '0.8rem', display: 'inline-block', fontWeight: 'bold' }}>
                          Rekomendasi UMKM
                        </div>
                      )}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>
      )}
    </main>
  );
};

export default Explore;
