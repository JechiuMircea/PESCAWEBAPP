import React from 'react'
import './Navigation.css'

interface NavigationProps {
  currentPage: string
  onPageChange: (page: string) => void
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange }) => {
  const menuItems = [
    { id: 'dashboard', label: '🏠 Dashboard', icon: '📊' },
    { id: 'catalog', label: '🐟 Catalogo', icon: '📚' },
    { id: 'identifier', label: '🔍 Identifica', icon: '🎯' },
    { id: 'database', label: '💾 Database', icon: '🗄️' }
  ]

  return (
    <nav className="app-navigation">
      <div className="nav-container">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-button ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onPageChange(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}

export default Navigation
