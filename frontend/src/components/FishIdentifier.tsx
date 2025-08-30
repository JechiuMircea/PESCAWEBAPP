import React, { useState } from 'react'
import './FishIdentifier.css'

interface FishCharacteristics {
  color: string
  shape: string
  habitat: string
  size: string
  fins: string
  mouth: string
}

interface SearchResult {
  id: number
  name: string
  scientificName: string
  matchScore: number
  image: string
  description: string
}

const FishIdentifier: React.FC = () => {
  const [characteristics, setCharacteristics] = useState<FishCharacteristics>({
    color: '',
    shape: '',
    habitat: '',
    size: '',
    fins: '',
    mouth: ''
  })

  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [isSearching, setIsSearching] = useState(false)

  // Opzioni disponibili per i filtri
  const options = {
    colors: ['Rosso', 'Blu', 'Verde', 'Giallo', 'Marrone', 'Grigio', 'Argento', 'Nero', 'Bianco'],
    shapes: ['Fusiforme', 'Piatta', 'Rotonda', 'Allungata', 'Triangolare', 'Ovaloide'],
    habitats: ['Acque dolci', 'Acque marine', 'Acque salmastre', 'Profondo', 'Superficiale'],
    sizes: ['Piccolo (< 10 cm)', 'Medio (10-30 cm)', 'Grande (30-60 cm)', 'Molto grande (> 60 cm)'],
    fins: ['Pinna dorsale', 'Pinna caudale', 'Pinne pettorali', 'Pinne ventrali', 'Pinna anale'],
    mouth: ['Superiore', 'Inferiore', 'Terminale', 'Sottostante', 'Protattile']
  }

  // Gestisce i cambiamenti nei campi
  const handleInputChange = (field: keyof FishCharacteristics, value: string) => {
    setCharacteristics(prev => ({
      ...prev,
      [field]: value
    }))
  }

  // Simula la ricerca di pesci
  const handleSearch = () => {
    setIsSearching(true)
    
    // Simula ricerca con delay
    setTimeout(() => {
      const mockResults: SearchResult[] = [
        {
          id: 1,
          name: 'Trota Fario',
          scientificName: 'Salmo trutta',
          matchScore: 85,
          image: '🐟',
          description: 'Pesce d\'acqua dolce con corpo fusiforme e colorazione marrone-rossastra.'
        },
        {
          id: 2,
          name: 'Carpa Comune',
          scientificName: 'Cyprinus carpio',
          matchScore: 72,
          image: '🐟',
          description: 'Pesce robusto con corpo allungato e colorazione dorata-marrone.'
        }
      ]
      
      setSearchResults(mockResults)
      setIsSearching(false)
    }, 1500)
  }

  // Verifica se la ricerca può essere eseguita
  const canSearch = Object.values(characteristics).some(value => value !== '')

  return (
    <div className="fish-identifier">
      <div className="identifier-header">
        <h2>🔍 Identificatore Pesci</h2>
        <p>Descrivi le caratteristiche del pesce che vuoi identificare</p>
      </div>

      {/* Form di identificazione */}
      <div className="identification-form">
        <div className="form-section">
          <h3>🎨 Caratteristiche Fisiche</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="color">Colore Principale:</label>
              <select
                id="color"
                value={characteristics.color}
                onChange={(e) => handleInputChange('color', e.target.value)}
                className="form-select"
              >
                <option value="">Seleziona colore...</option>
                {options.colors.map(color => (
                  <option key={color} value={color}>{color}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="shape">Forma del Corpo:</label>
              <select
                id="shape"
                value={characteristics.shape}
                onChange={(e) => handleInputChange('shape', e.target.value)}
                className="form-select"
              >
                <option value="">Seleziona forma...</option>
                {options.shapes.map(shape => (
                  <option key={shape} value={shape}>{shape}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="size">Dimensione:</label>
              <select
                id="size"
                value={characteristics.size}
                onChange={(e) => handleInputChange('size', e.target.value)}
                className="form-select"
              >
                <option value="">Seleziona dimensione...</option>
                {options.sizes.map(size => (
                  <option key={size} value={size}>{size}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="habitat">Habitat:</label>
              <select
                id="habitat"
                value={characteristics.habitat}
                onChange={(e) => handleInputChange('habitat', e.target.value)}
                className="form-select"
              >
                <option value="">Seleziona habitat...</option>
                {options.habitats.map(habitat => (
                  <option key={habitat} value={habitat}>{habitat}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="fins">Caratteristiche Pinne:</label>
              <select
                id="fins"
                value={characteristics.fins}
                onChange={(e) => handleInputChange('fins', e.target.value)}
                className="form-select"
              >
                <option value="">Seleziona caratteristica...</option>
                {options.fins.map(fin => (
                  <option key={fin} value={fin}>{fin}</option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="mouth">Posizione Bocca:</label>
              <select
                id="mouth"
                value={characteristics.mouth}
                onChange={(e) => handleInputChange('mouth', e.target.value)}
                className="form-select"
              >
                <option value="">Seleziona posizione...</option>
                {options.mouth.map(mouth => (
                  <option key={mouth} value={mouth}>{mouth}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Pulsante di ricerca */}
        <div className="search-actions">
          <button
            onClick={handleSearch}
            disabled={!canSearch || isSearching}
            className="search-button"
          >
            {isSearching ? '🔍 Ricerca in corso...' : '🔍 Identifica Pesce'}
          </button>
          
          {!canSearch && (
            <p className="form-hint">
              💡 Compila almeno un campo per iniziare la ricerca
            </p>
          )}
        </div>
      </div>

      {/* Risultati della ricerca */}
      {searchResults.length > 0 && (
        <div className="search-results">
          <h3>🎯 Risultati Identificazione</h3>
          
          <div className="results-list">
            {searchResults.map(result => (
              <div key={result.id} className="result-card">
                <div className="result-header">
                  <span className="result-image">{result.image}</span>
                  <div className="result-info">
                    <h4>{result.name}</h4>
                    <p className="scientific-name">{result.scientificName}</p>
                  </div>
                  <div className="match-score">
                    <span className="score-label">Match:</span>
                    <span className="score-value">{result.matchScore}%</span>
                  </div>
                </div>
                
                <p className="result-description">{result.description}</p>
                
                <div className="result-actions">
                  <button className="action-button">📚 Vedi Dettagli</button>
                  <button className="action-button">🖼️ Confronta Immagini</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stato di ricerca */}
      {isSearching && (
        <div className="searching-state">
          <div className="loading-spinner"></div>
          <p>🔍 Analizzando caratteristiche e cercando nel database...</p>
        </div>
      )}
    </div>
  )
}

export default FishIdentifier
