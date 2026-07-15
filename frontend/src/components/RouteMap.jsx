import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Navigation, Star } from 'lucide-react';

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

const RouteMap = ({ destinasiUtama, umkmSekitar }) => {
  // Hanya ambil destinasi yang memiliki latitude dan longitude
  const validDestinasi = destinasiUtama.filter(d => d.latitude && d.longitude);
  const validUmkm = umkmSekitar.filter(u => u.latitude && u.longitude);
  
  if (validDestinasi.length === 0 && validUmkm.length === 0) {
    return null;
  }

  // Tentukan pusat peta (gunakan titik pertama destinasi utama atau default Danau Toba)
  const center = validDestinasi.length > 0 
    ? [validDestinasi[0].latitude, validDestinasi[0].longitude] 
    : (validUmkm.length > 0 ? [validUmkm[0].latitude, validUmkm[0].longitude] : [2.6105, 98.8106]);

  // Ekstrak koordinat untuk rute (Polyline) dari destinasi utama
  const routeCoordinates = validDestinasi.map(d => [d.latitude, d.longitude]);

  return (
    <div className="route-map-wrapper glass-panel" style={{ height: '400px', width: '100%', borderRadius: 'var(--radius-lg)', overflow: 'hidden', padding: '0.5rem', marginTop: '2rem' }}>
      <MapContainer 
        center={center} 
        zoom={11} 
        style={{ height: '100%', width: '100%', borderRadius: 'calc(var(--radius-lg) - 0.5rem)' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Draw Polyline untuk rute Destinasi Utama */}
        {routeCoordinates.length > 1 && (
          <Polyline 
            positions={routeCoordinates} 
            color="#0ea5e9" 
            weight={4} 
            dashArray="10, 10" 
            opacity={0.8}
          />
        )}

        {/* Marker Destinasi Utama */}
        {validDestinasi.map((dest, idx) => (
          <Marker 
            key={`dest-${dest.id}`} 
            position={[dest.latitude, dest.longitude]} 
            icon={wisataIcon}
          >
            <Popup>
              <div style={{ minWidth: '150px' }}>
                <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--color-primary-dark)' }}>
                  {idx + 1}. {dest.nama}
                </h4>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.5rem', fontSize: '0.85rem', color: '#64748b' }}>
                  <Navigation size={12} /> {dest.kecamatan}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.85rem', color: '#64748b' }}>
                  <Star size={12} fill="#fbbf24" color="#fbbf24" /> {dest.rating}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Marker UMKM */}
        {validUmkm.map(umkm => (
          <Marker 
            key={`umkm-${umkm.id}`} 
            position={[umkm.latitude, umkm.longitude]} 
            icon={umkmIcon}
          >
            <Popup>
              <div style={{ minWidth: '150px' }}>
                <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--color-accent-dark, #16a34a)' }}>
                  {umkm.nama}
                </h4>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.5rem', fontSize: '0.85rem', color: '#64748b' }}>
                  <Navigation size={12} /> {umkm.kecamatan}
                </div>
                <div style={{ marginTop: '0.5rem', padding: '0.25rem 0.5rem', background: '#dcfce7', color: '#166534', borderRadius: '4px', fontSize: '0.75rem', display: 'inline-block', fontWeight: 'bold' }}>
                  Rekomendasi UMKM
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default RouteMap;
