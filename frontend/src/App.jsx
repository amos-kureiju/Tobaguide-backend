import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Compass } from 'lucide-react';
import Home from './pages/Home';
import Explore from './pages/Explore';
import About from './pages/About';
import Chatbot from './components/Chatbot';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Navbar */}
        <nav className="navbar glass-panel">
          <div className="container nav-content">
            <div className="logo">
              <Compass size={28} color="var(--color-primary)" />
              <h1>TobaRoute <span className="highlight">AI</span></h1>
            </div>
            <div className="nav-links">
              <NavLink 
                to="/" 
                className={({ isActive }) => (isActive ? 'active' : '')}
                end
              >
                Beranda
              </NavLink>
              <NavLink 
                to="/explore" 
                className={({ isActive }) => (isActive ? 'active' : '')}
              >
                Jelajah
              </NavLink>
              <NavLink 
                to="/about" 
                className={({ isActive }) => (isActive ? 'active' : '')}
              >
                Tentang
              </NavLink>
            </div>
          </div>
        </nav>

        {/* Page Content */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/explore" element={<Explore />} />
          <Route path="/about" element={<About />} />
        </Routes>

        <footer className="footer">
          <p>&copy; 2026 TobaRoute AI. Dibangun untuk mendukung Keadilan Pariwisata Danau Toba.</p>
        </footer>

        {/* Global Chatbot */}
        <Chatbot />
      </div>
    </Router>
  );
}

export default App;
