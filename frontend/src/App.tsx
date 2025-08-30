import { useState } from 'react'
import './App.css'

// Componenti principali della Pesca WebApp
import Header from './components/Header'
import Navigation from './components/Navigation'
import Dashboard from './components/Dashboard'
import FishCatalog from './components/FishCatalog'
import FishIdentifier from './components/FishIdentifier'
import DatabaseManager from './components/DatabaseManager'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [isLoading, setIsLoading] = useState(false)

  // Gestione navigazione tra pagine
  const handlePageChange = (page: string) => {
    setIsLoading(true)
    setCurrentPage(page)
    // Simula caricamento per transizioni fluide
    setTimeout(() => setIsLoading(false), 300)
  }

  // Renderizza la pagina corrente
  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'catalog':
        return <FishCatalog />
      case 'identifier':
        return <FishIdentifier />
      case 'database':
        return <DatabaseManager />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="pesca-webapp">
      {/* Header principale con logo e titolo */}
      <Header />
      
      {/* Navigazione principale */}
      <Navigation 
        currentPage={currentPage} 
        onPageChange={handlePageChange} 
      />
      
      {/* Contenuto principale con loading state */}
      <main className="main-content">
        {isLoading ? (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Caricamento...</p>
          </div>
        ) : (
          renderCurrentPage()
        )}
      </main>
      
      {/* Footer con informazioni */}
      <footer className="app-footer">
        <p>&copy; 2025 Pesca WebApp - Identificazione e Gestione Pesci</p>
        <p>Integrato con FishBase Database</p>
      </footer>
    </div>
  )
}

export default App
