import React, { useState, useEffect } from 'react'
import './DatabaseManager.css'

interface DatabaseStatus {
  isOnline: boolean
  lastSync: string
  totalRecords: number
  lastUpdate: string
  syncStatus: 'idle' | 'syncing' | 'error' | 'success'
}

interface DatabaseOperation {
  id: string
  type: 'import' | 'export' | 'sync' | 'backup'
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  message: string
  timestamp: string
}

const DatabaseManager: React.FC = () => {
  const [dbStatus, setDbStatus] = useState<DatabaseStatus>({
    isOnline: true,
    lastSync: '2025-08-30 17:15:00',
    totalRecords: 15,
    lastUpdate: '2025-08-30 16:45:00',
    syncStatus: 'idle'
  })

  const [operations, setOperations] = useState<DatabaseOperation[]>([])
  const [isPerformingOperation, setIsPerformingOperation] = useState(false)

  // Simula il controllo dello stato del database
  useEffect(() => {
    const checkDatabaseStatus = () => {
      // Simula controllo stato
      setDbStatus(prev => ({
        ...prev,
        isOnline: Math.random() > 0.1, // 90% probabilità di essere online
        lastUpdate: new Date().toLocaleString('it-IT')
      }))
    }

    const interval = setInterval(checkDatabaseStatus, 30000) // Controlla ogni 30 secondi
    return () => clearInterval(interval)
  }, [])

  // Simula operazione di sincronizzazione
  const handleSync = () => {
    if (isPerformingOperation) return

    setIsPerformingOperation(true)
    setDbStatus(prev => ({ ...prev, syncStatus: 'syncing' }))

    const operationId = `sync_${Date.now()}`
    const newOperation: DatabaseOperation = {
      id: operationId,
      type: 'sync',
      status: 'running',
      progress: 0,
      message: 'Sincronizzazione in corso...',
      timestamp: new Date().toLocaleString('it-IT')
    }

    setOperations(prev => [...prev, newOperation])

    // Simula progresso
    let progress = 0
    const progressInterval = setInterval(() => {
      progress += Math.random() * 20
      if (progress >= 100) {
        progress = 100
        clearInterval(progressInterval)
        
        // Completa l'operazione
        setOperations(prev => prev.map(op => 
          op.id === operationId 
            ? { ...op, status: 'completed', progress: 100, message: 'Sincronizzazione completata' }
            : op
        ))
        
        setDbStatus(prev => ({
          ...prev,
          syncStatus: 'success',
          lastSync: new Date().toLocaleString('it-IT'),
          totalRecords: prev.totalRecords + Math.floor(Math.random() * 5)
        }))
        
        setIsPerformingOperation(false)
        
        // Reset status dopo 3 secondi
        setTimeout(() => {
          setDbStatus(prev => ({ ...prev, syncStatus: 'idle' }))
        }, 3000)
      } else {
        setOperations(prev => prev.map(op => 
          op.id === operationId 
            ? { ...op, progress: Math.round(progress) }
            : op
        ))
      }
    }, 200)
  }

  // Simula backup del database
  const handleBackup = () => {
    if (isPerformingOperation) return

    setIsPerformingOperation(true)
    
    const operationId = `backup_${Date.now()}`
    const newOperation: DatabaseOperation = {
      id: operationId,
      type: 'backup',
      status: 'running',
      progress: 0,
      message: 'Backup in corso...',
      timestamp: new Date().toLocaleString('it-IT')
    }

    setOperations(prev => [...prev, newOperation])

    // Simula backup
    setTimeout(() => {
      setOperations(prev => prev.map(op => 
        op.id === operationId 
          ? { ...op, status: 'completed', progress: 100, message: 'Backup completato' }
          : op
      ))
      setIsPerformingOperation(false)
    }, 2000)
  }

  // Simula export dei dati
  const handleExport = () => {
    if (isPerformingOperation) return

    setIsPerformingOperation(true)
    
    const operationId = `export_${Date.now()}`
    const newOperation: DatabaseOperation = {
      id: operationId,
      type: 'export',
      status: 'running',
      progress: 0,
      message: 'Export in corso...',
      timestamp: new Date().toLocaleString('it-IT')
    }

    setOperations(prev => [...prev, newOperation])

    // Simula export
    setTimeout(() => {
      setOperations(prev => prev.map(op => 
        op.id === operationId 
          ? { ...op, status: 'completed', progress: 100, message: 'Export completato' }
          : op
      ))
      setIsPerformingOperation(false)
    }, 1500)
  }

  return (
    <div className="database-manager">
      <div className="manager-header">
        <h2>💾 Gestione Database</h2>
        <p>Monitora e gestisci il database della Pesca WebApp</p>
      </div>

      {/* Stato del database */}
      <div className="database-status">
        <h3>📊 Stato Database</h3>
        
        <div className="status-grid">
          <div className="status-card">
            <div className="status-indicator">
              <span className={`status-dot ${dbStatus.isOnline ? 'online' : 'offline'}`}></span>
              <span className="status-text">
                {dbStatus.isOnline ? '🟢 Online' : '🔴 Offline'}
              </span>
            </div>
          </div>
          
          <div className="status-card">
            <h4>Ultima Sincronizzazione</h4>
            <p>{dbStatus.lastSync}</p>
          </div>
          
          <div className="status-card">
            <h4>Record Totali</h4>
            <p className="record-count">{dbStatus.totalRecords}</p>
          </div>
          
          <div className="status-card">
            <h4>Ultimo Aggiornamento</h4>
            <p>{dbStatus.lastUpdate}</p>
          </div>
        </div>
      </div>

      {/* Operazioni database */}
      <div className="database-operations">
        <h3>🚀 Operazioni Database</h3>
        
        <div className="operations-grid">
          <button
            onClick={handleSync}
            disabled={isPerformingOperation || dbStatus.syncStatus === 'syncing'}
            className={`operation-button sync ${dbStatus.syncStatus}`}
          >
            🔄 Sincronizza con FishBase
          </button>
          
          <button
            onClick={handleBackup}
            disabled={isPerformingOperation}
            className="operation-button backup"
          >
            💾 Crea Backup
          </button>
          
          <button
            onClick={handleExport}
            disabled={isPerformingOperation}
            className="operation-button export"
          >
            📤 Esporta Dati
          </button>
        </div>

        {/* Indicatore stato sincronizzazione */}
        {dbStatus.syncStatus === 'syncing' && (
          <div className="sync-status">
            <div className="sync-spinner"></div>
            <p>Sincronizzazione in corso...</p>
          </div>
        )}
        
        {dbStatus.syncStatus === 'success' && (
          <div className="sync-success">
            <span className="success-icon">✅</span>
            <p>Sincronizzazione completata con successo!</p>
          </div>
        )}
      </div>

      {/* Cronologia operazioni */}
      <div className="operations-history">
        <h3>📋 Cronologia Operazioni</h3>
        
        {operations.length === 0 ? (
          <p className="no-operations">Nessuna operazione eseguita</p>
        ) : (
          <div className="operations-list">
            {operations.slice(-5).reverse().map(operation => (
              <div key={operation.id} className={`operation-item ${operation.status}`}>
                <div className="operation-header">
                  <span className="operation-type">{operation.type.toUpperCase()}</span>
                  <span className="operation-time">{operation.timestamp}</span>
                </div>
                
                <div className="operation-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${operation.progress}%` }}
                    ></div>
                  </div>
                  <span className="progress-text">{operation.progress}%</span>
                </div>
                
                <div className="operation-message">{operation.message}</div>
                
                <div className="operation-status">
                  <span className={`status-badge ${operation.status}`}>
                    {operation.status === 'pending' && '⏳ In attesa'}
                    {operation.status === 'running' && '🔄 In corso'}
                    {operation.status === 'completed' && '✅ Completato'}
                    {operation.status === 'failed' && '❌ Fallito'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Informazioni FishBase */}
      <div className="fishbase-info">
        <h3>🌊 Informazioni FishBase</h3>
        <div className="info-content">
          <p>
            Il database è integrato con FishBase, la più completa banca dati 
            mondiale sui pesci. La sincronizzazione mantiene aggiornate le informazioni 
            su specie, habitat e distribuzione geografica.
          </p>
          <div className="integration-stats">
            <span className="stat">🌍 35.000+ specie</span>
            <span className="stat">📊 Dati scientifici</span>
            <span className="stat">🖼️ Immagini HD</span>
            <span className="stat">🗺️ Distribuzione</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DatabaseManager
