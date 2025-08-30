import React from 'react'
import './Header.css'

const Header: React.FC = () => {
  return (
    <header className="app-header">
      <div className="header-content">
        {/* Logo e titolo principale */}
        <div className="header-brand">
          <div className="logo-container">
            <span className="logo-icon">🎣</span>
          </div>
          <h1 className="app-title">Pesca WebApp</h1>
          <p className="app-subtitle">Identificazione e Gestione Pesci</p>
        </div>
        
        {/* Informazioni aggiuntive */}
        <div className="header-info">
          <div className="database-status">
            <span className="status-indicator online"></span>
            <span className="status-text">Database Online</span>
          </div>
          <div className="fishbase-integration">
            <span className="integration-icon">🌊</span>
            <span className="integration-text">FishBase Integrato</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
