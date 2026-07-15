import { useEffect } from "react";
import L from "leaflet";
import "leaflet-routing-machine";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import { useMap } from "react-leaflet";

const RoutingMachine = ({ waypoints }) => {
  const map = useMap();

  useEffect(() => {
    if (!map) return;
    if (!waypoints || waypoints.length < 2) return;

    const routingControl = L.Routing.control({
      waypoints: waypoints.map(wp => L.latLng(wp[0], wp[1])),
      routeWhileDragging: false,
      addWaypoints: false,
      fitSelectedRoutes: true,
      showAlternatives: false,
      // Menonaktifkan pembuatan marker default dari routing machine karena kita sudah punya marker sendiri
      createMarker: function() { return null; },
      lineOptions: {
        styles: [{ color: "#0ea5e9", opacity: 0.8, weight: 5 }]
      },
      show: false // Menyembunyikan panel instruksi rute
    }).addTo(map);

    // Menyembunyikan container instruksi secara paksa via DOM (jika show: false gagal)
    const container = routingControl.getContainer();
    if (container) {
      container.style.display = 'none';
    }

    return () => {
      if (map && routingControl) {
        map.removeControl(routingControl);
      }
    };
  }, [map, waypoints]);

  return null;
};

export default RoutingMachine;
