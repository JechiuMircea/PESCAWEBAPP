import React, { useState } from 'react'
import './FishCatalog.css'

interface FishSpecies {
  id: number
  name: string
  scientificName: string
  family: string
  habitat: string
  maxLength: number
  image: string
  description: string
}

const FishCatalog: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFamily, setSelectedFamily] = useState('all')
  const [selectedHabitat, setSelectedHabitat] = useState('all')

  // Dati di esempio per le specie
  const fishSpecies: FishSpecies[] = [
    {
      id: 1,
      name: 'Trota Fario',
      scientificName: 'Salmo trutta',
      family: 'Salmonidae',
      habitat: 'Acque dolci',
      maxLength: 60,
      image: '🐟',
      description: 'Pesce d\'acqua dolce molto apprezzato per la pesca sportiva.'
    },
    {
      id: 2,
      name: 'Carpa Comune',
      scientificName: 'Cyprinus carpio',
      family: 'Cyprinidae',
      habitat: 'Acque dolci',
      maxLength: 120,
      image: '🐟',
      description: 'Pesce robusto e longevo, molto diffuso in Europa.'
    },
    {
      id: 3,
      name: 'Branzino',
      scientificName: 'Dicentrarchus labrax',
      family: 'Moronidae',
      habitat: 'Acque marine',
      maxLength: 100,
      image: '🐟',
      description: 'Pesce marino pregiato, molto apprezzato in cucina.'
    }
  ]

  // Filtri disponibili
  const families = ['all', ...Array.from(new Set(fishSpecies.map(fish => fish.family)))]
  const habitats = ['all', ...Array.from(new Set(fishSpecies.map(fish => fish.habitat)))]

  // Filtra le specie
  const filteredSpecies = fishSpecies.filter(fish => {
    const matchesSearch = fish.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         fish.scientificName.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFamily = selectedFamily === 'all' || fish.family === selectedFamily
    const matchesHabitat = selectedHabitat === 'all' || fish.habitat === selectedHabitat
    
    return matchesSearch && matchesFamily && matchesHabitat
  })

  return (
    <div className="fish-catalog">
      <div className="catalog-header">
        <h2>🐟 Catalogo Specie Pesci</h2>
        <p>Esplora e scopri le specie disponibili nel database</p>
      </div>

      {/* Filtri di ricerca */}
      <div className="search-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="🔍 Cerca per nome o nome scientifico..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-controls">
          <select
            value={selectedFamily}
            onChange={(e) => setSelectedFamily(e.target.value)}
            className="filter-select"
          >
            {families.map(family => (
              <option key={family} value={family}>
                {family === 'all' ? '🏠 Tutte le Famiglie' : family}
              </option>
            ))}
          </select>
          
          <select
            value={selectedHabitat}
            onChange={(e) => setSelectedHabitat(e.target.value)}
            className="filter-select"
          >
            {habitats.map(habitat => (
              <option key={habitat} value={habitat}>
                {habitat === 'all' ? '🌊 Tutti gli Habitat' : habitat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Risultati ricerca */}
      <div className="catalog-results">
        <div className="results-header">
          <h3>📊 Risultati: {filteredSpecies.length} specie trovate</h3>
        </div>
        
        <div className="species-grid">
          {filteredSpecies.map(fish => (
            <div key={fish.id} className="species-card">
              <div className="species-image">
                <span className="fish-emoji">{fish.image}</span>
              </div>
              
              <div className="species-info">
                <h4 className="species-name">{fish.name}</h4>
                <p className="scientific-name">{fish.scientificName}</p>
                
                <div className="species-details">
                  <span className="detail-item">
                    <strong>Famiglia:</strong> {fish.family}
                  </span>
                  <span className="detail-item">
                    <strong>Habitat:</strong> {fish.habitat}
                  </span>
                  <span className="detail-item">
                    <strong>Lunghezza Max:</strong> {fish.maxLength} cm
                  </span>
                </div>
                
                <p className="species-description">{fish.description}</p>
              </div>
            </div>
          ))}
        </div>
        
        {filteredSpecies.length === 0 && (
          <div className="no-results">
            <p>🔍 Nessuna specie trovata con i filtri selezionati</p>
            <p>Prova a modificare i criteri di ricerca</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default FishCatalog
