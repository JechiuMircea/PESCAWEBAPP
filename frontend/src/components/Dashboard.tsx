import React from 'react'
import './Dashboard.css'

const Dashboard: React.FC = () => {
  // Dati di esempio per il dashboard
  const stats = {
    totalSpecies: 15,
    families: 11,
    habitats: 13,
    lastUpdate: '2025-08-30'
  }

  const quickActions = [
    { id: 'search', label: '🔍 Cerca Pesce', action: 'identifier', icon: '🎯' },
    { id: 'browse', label: '📚 Sfoglia Catalogo', action: 'catalog', icon: '🐟' },
    { id: 'stats', label: '📊 Statistiche', action: 'database', icon: '💾' }
  ]

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>🏠 Dashboard - Benvenuto nella Pesca WebApp</h2>
        <p className="dashboard-description">
          La tua guida completa per l'identificazione e la gestione dei pesci
        </p>
      </div>

      {/* Statistiche principali */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🐟</div>
          <div className="stat-content">
            <h3>Specie Totali</h3>
            <p className="stat-number">{stats.totalSpecies}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🏠</div>
          <div className="stat-content">
            <h3>Famiglie</h3>
            <p className="stat-number">{stats.families}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🌊</div>
          <div className="stat-content">
            <h3>Habitat</h3>
            <p className="stat-number">{stats.habitats}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🕒</div>
          <div className="stat-content">
            <h3>Ultimo Aggiornamento</h3>
            <p className="stat-date">{stats.lastUpdate}</p>
          </div>
        </div>
      </div>

      {/* Azioni rapide */}
      <div className="quick-actions">
        <h3>🚀 Azioni Rapide</h3>
        <div className="actions-grid">
          {quickActions.map((action) => (
            <div key={action.id} className="action-card">
              <div className="action-icon">{action.icon}</div>
              <h4>{action.label}</h4>
              <p>Accesso rapido alle funzionalità principali</p>
            </div>
          ))}
        </div>
      </div>

      {/* Informazioni FishBase */}
      <div className="fishbase-info">
        <h3>🌊 Integrazione FishBase</h3>
        <div className="info-content">
          <p>
            La Pesca WebApp è integrata con il database FishBase, 
            fornendo informazioni accurate e aggiornate su oltre 35.000 specie di pesci.
          </p>
          <div className="integration-features">
            <span className="feature">✅ Dati scientifici</span>
            <span className="feature">✅ Immagini ad alta qualità</span>
            <span className="feature">✅ Distribuzione geografica</span>
            <span className="feature">✅ Habitat e comportamento</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
