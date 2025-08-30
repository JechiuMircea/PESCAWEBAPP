# 🚀 Guida Sviluppo Frontend

## 🎯 Setup Ambiente di Sviluppo

### **Prerequisiti**
- ✅ Node.js 18+ installato
- ✅ npm o yarn disponibile
- ✅ Git configurato
- ✅ Backend FastAPI attivo (porta 8080)

### **Installazione Dipendenze**
```bash
cd frontend
npm install
```

### **Avvio Server Sviluppo**
```bash
npm run dev
```
**Risultato**: Server attivo su http://localhost:5173

## 🏗️ Struttura Progetto Attuale

### **File Esistenti**
```
frontend/
├── src/
│   ├── App.tsx              # Componente principale
│   ├── App.css              # Stili componente principale
│   ├── index.css            # Stili globali
│   ├── main.tsx             # Entry point React
│   └── vite-env.d.ts        # Tipi Vite
├── public/                  # File statici pubblici
├── package.json             # Dipendenze e script
├── tsconfig.json            # Configurazione TypeScript
├── vite.config.ts           # Configurazione Vite
└── eslint.config.js         # Configurazione ESLint
```

### **Configurazioni Attive**
- **Vite**: Build tool con hot reload
- **TypeScript**: Tipizzazione statica
- **ESLint**: Code quality e linting
- **React 19**: Ultima versione con hooks

## 🔧 Comandi Disponibili

### **Script NPM**
```bash
npm run dev          # Server sviluppo con hot reload
npm run build        # Build produzione
npm run preview      # Preview build produzione
npm run lint         # Esecuzione ESLint
```

### **Comandi Utili**
```bash
# Verifica dipendenze
npm list --depth=0

# Aggiornamento dipendenze
npm update

# Installazione nuova dipendenza
npm install nome-pacchetto

# Installazione dipendenza sviluppo
npm install --save-dev nome-pacchetto
```

## 📱 Sviluppo Componenti

### **1. Creazione Componente Base**
```typescript
// src/components/ui/Button/Button.tsx
import React from 'react';
import './Button.css';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false,
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
```

### **2. Styling Componente**
```css
/* src/components/ui/Button/Button.css */
.btn {
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary {
  background-color: #1E40AF;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1E3A8A;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

### **3. Export e Import**
```typescript
// src/components/ui/Button/index.ts
export { Button } from './Button';

// Utilizzo in altri componenti
import { Button } from '@/components/ui/Button';
```

## 🔗 Integrazione Backend

### **1. Configurazione API Service**
```typescript
// src/services/api/config.ts
export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8080',
  TIMEOUT: 10000,
  ENDPOINTS: {
    HEALTH: '/health',
    SPECIES: '/species',
    IDENTIFY: '/identify',
  },
};
```

### **2. Custom Hook per API**
```typescript
// src/hooks/useApi.ts
import { useState, useEffect } from 'react';
import { API_CONFIG } from '@/services/api/config';

interface UseApiOptions<T> {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: any;
  dependencies?: any[];
}

export function useApi<T>({ url, method = 'GET', body, dependencies = [] }: UseApiOptions<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${url}`, {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: body ? JSON.stringify(body) : undefined,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, loading, error };
}
```

### **3. Utilizzo Hook API**
```typescript
// src/components/features/SpeciesCatalog/SpeciesCatalog.tsx
import { useApi } from '@/hooks/useApi';
import { API_CONFIG } from '@/services/api/config';

export const SpeciesCatalog: React.FC = () => {
  const { data: species, loading, error } = useApi({
    url: API_CONFIG.ENDPOINTS.SPECIES,
    dependencies: [],
  });

  if (loading) return <div>Caricamento specie...</div>;
  if (error) return <div>Errore: {error}</div>;
  if (!species) return <div>Nessuna specie trovata</div>;

  return (
    <div className="species-catalog">
      {species.map((specie) => (
        <div key={specie.id} className="species-card">
          <h3>{specie.nome}</h3>
          <p>{specie.famiglia}</p>
        </div>
      ))}
    </div>
  );
};
```

## 🎨 Styling e CSS

### **1. CSS Modules (Raccomandato)**
```typescript
// src/components/Feature/Feature.module.css
.feature {
  padding: 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.featureTitle {
  color: #1E40AF;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

// Utilizzo
import styles from './Feature.module.css';

<div className={styles.feature}>
  <h2 className={styles.featureTitle}>Titolo</h2>
</div>
```

### **2. CSS-in-JS (Alternativa)**
```typescript
// Con styled-components o emotion
import styled from 'styled-components';

const StyledButton = styled.button`
  background-color: ${props => props.variant === 'primary' ? '#1E40AF' : '#6B7280'};
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  
  &:hover {
    opacity: 0.9;
  }
`;
```

## 📱 Responsive Design

### **1. CSS Media Queries**
```css
/* Mobile First approach */
.container {
  padding: 16px;
  max-width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    max-width: 720px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 960px;
  }
}
```

### **2. Hook per Responsive**
```typescript
// src/hooks/useResponsive.ts
import { useState, useEffect } from 'react';

export function useResponsive() {
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [isDesktop, setIsDesktop] = useState(false);

  useEffect(() => {
    const checkSize = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);
      setIsDesktop(width >= 1024);
    };

    checkSize();
    window.addEventListener('resize', checkSize);
    
    return () => window.removeEventListener('resize', checkSize);
  }, []);

  return { isMobile, isTablet, isDesktop };
}
```

## 🧪 Testing

### **1. Setup Testing**
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

### **2. Test Componente**
```typescript
// src/components/ui/Button/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## 🚀 Build e Deploy

### **1. Build Produzione**
```bash
npm run build
```
**Risultato**: Cartella `dist/` con file ottimizzati

### **2. Preview Build**
```bash
npm run preview
```
**Risultato**: Server locale per testare build produzione

### **3. Analisi Bundle**
```bash
npm install --save-dev vite-bundle-analyzer
npx vite-bundle-analyzer dist/stats.html
```

## 🔍 Debug e Troubleshooting

### **1. Problemi Comuni**
- **Porta 5173 occupata**: Cambia porta in `vite.config.ts`
- **Hot reload non funziona**: Verifica firewall/antivirus
- **Errori TypeScript**: Controlla `tsconfig.json` e tipi

### **2. DevTools**
- **React DevTools**: Estensione browser per debugging
- **Vite DevTools**: Integrati nel browser per performance
- **Console Browser**: Log e errori runtime

### **3. Performance**
- **Lighthouse**: Analisi performance e best practices
- **React Profiler**: Profiling componenti
- **Bundle Analyzer**: Analisi dimensioni bundle

## 📚 Risorse Utili

### **Documentazione Ufficiale**
- [React Docs](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)

### **Librerie Consigliate**
- **State Management**: Zustand, Redux Toolkit
- **Routing**: React Router DOM
- **Forms**: React Hook Form, Formik
- **UI Components**: Radix UI, Headless UI

## 🎨 Stile del Codice e Standard

### **📚 Guida Completa Stile:**
- **📖 [Guida Stile Codice Frontend](frontend-code-style.md)** - Regole e standard del progetto
- **🎯 Stile adottato:** Vite Moderno (senza punto e virgola)
- **⚠️ Importante:** Leggere la guida per evitare ambiguità

### **🔧 Strumenti di Controllo Qualità:**
- **Prettier** - Formattazione automatica
- **ESLint** - Controllo logica e best practices
- **Jest** - Testing framework
- **Husky** - Pre-commit hooks
- **Lint-staged** - Controllo file modificati

---

**Prossimo**: [Backend Integration Guide](../api/endpoints.md)
