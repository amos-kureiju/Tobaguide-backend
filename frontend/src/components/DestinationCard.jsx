import React from 'react';
import { MapPin, Star, Navigation } from 'lucide-react';
import './DestinationCard.css';

const DestinationCard = ({ dest, isUmkm }) => {
  return (
    <div className={`card destination-card ${isUmkm ? 'umkm-card' : ''}`}>
      {dest.gambar_url ? (
        <img src={dest.gambar_url} alt={dest.nama} className="card-image" />
      ) : (
        <div className="card-image-placeholder">
          <MapPin size={48} color="#64748b" />
        </div>
      )}
      <div className="card-content">
        <div className="card-header">
          <h3 className="card-title">{dest.nama}</h3>
          {isUmkm && <span className="badge-umkm">Recommended UMKM</span>}
        </div>
        <div className="card-meta">
          <span className="meta-item">
            <Navigation size={14} />
            {dest.kecamatan}
          </span>
          <span className="meta-item rating">
            <Star size={14} fill="#fbbf24" color="#fbbf24" />
            {dest.rating} ({dest.jumlah_ulasan})
          </span>
        </div>
        <p className="card-description">{dest.deskripsi_singkat}</p>
        <p className="card-address">{dest.nama_jalan}</p>
      </div>
    </div>
  );
};

export default DestinationCard;
