# 🎨 Guida Stile Codice Frontend

## 🎯 Panoramica

**Pesca WebApp Frontend** adotta uno **stile di codice moderno** basato sui framework React + Vite, con configurazioni personalizzate per mantenere la coerenza del progetto.

## 🚀 Stile Adottato: **Vite Moderno**

### **✅ Caratteristiche principali:**
- **Nessun punto e virgola** (`;`) alla fine delle istruzioni
- **Stile pulito e minimalista** 
- **Standard moderno** di React 19 + Vite
- **ASI (Automatic Semicolon Insertion)** sfruttato attivamente

### **⚠️ Differenze dagli standard aziendali tradizionali:**
- **Molte aziende** usano punto e virgola esplicito
- **Standard enterprise** spesso richiedono `;` per chiarezza
- **Team tradizionali** potrebbero non essere familiari con questo stile

## 📋 Regole di Formattazione

### **1. Punto e Virgola (`;`)**
```typescript
// ❌ NON fare questo (stile tradizionale)
const nome = "Mario";
const eta = 25;

// ✅ FARE questo (stile Vite)
const nome = "Mario"
const eta = 25
```

### **2. Import/Export**
```typescript
// ❌ NON fare questo
import { useState } from 'react';
import './App.css';

// ✅ FARE questo
import { useState } from 'react'
import './App.css'
```

### **3. Funzioni e Componenti**
```typescript
// ❌ NON fare questo
function App() {
  return <div>Hello</div>;
}

// ✅ FARE questo
function App() {
  return <div>Hello</div>
}
```

## ⚠️ Casi Speciali e Soluzioni

### **1. IIFE (Immediately Invoked Function Expression)**
```typescript
// ❌ PROBLEMA: può causare ambiguità
const nome = "Mario"
(function() { console.log("IIFE") })()

// ✅ SOLUZIONE 1: Parentesi all'inizio della riga
const nome = "Mario"
;(function() { console.log("IIFE") })()

// ✅ SOLUZIONE 2: Riga vuota prima
const nome = "Mario"

(function() { console.log("IIFE") })()

// ✅ SOLUZIONE 3: Punto e virgola solo dove serve
const nome = "Mario";
(function() { console.log("IIFE") })()
```

### **2. Array/Array Literals**
```typescript
// ❌ PROBLEMA: può causare ambiguità
const items = [1, 2, 3]
[4, 5, 6].forEach(item => console.log(item))

// ✅ SOLUZIONE: Parentesi all'inizio
const items = [1, 2, 3]
;[4, 5, 6].forEach(item => console.log(item))
```

### **3. Template Literals**
```typescript
// ❌ PROBLEMA: può causare ambiguità
const tag = "div"
`<${tag}>Hello</${tag}>`

// ✅ SOLUZIONE: Parentesi all'inizio
const tag = "div"
;`<${tag}>Hello</${tag}>`
```

## 🛠️ Strumenti di Controllo Qualità

### **✅ Strumenti configurati per lo stile Vite:**

| **Strumento** | **Configurazione** | **Scopo** |
|---------------|-------------------|-----------|
| **Prettier** | `"semi": false` | Formattazione automatica |
| **ESLint** | Regole React + TypeScript | Controllo logica |
| **Husky** | Pre-commit hooks | Controllo automatico |
| **Lint-staged** | Controllo file modificati | Qualità pre-commit |

### **🔧 Comandi disponibili:**
```bash
# Verifica formattazione
npm run format:check

# Correggi formattazione automaticamente
npm run format

# Controllo qualità completo
npm run quality

# Controllo qualità + correzioni
npm run quality:fix
```

## 📚 Risorse per Sviluppatori

### **1. Documentazione ufficiale:**
- [Prettier - Semicolons](https://prettier.io/docs/en/options.html#semicolons)
- [JavaScript ASI](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#automatic_semicolon_insertion)

### **2. Best Practices per il progetto:**
- **Sempre** usare Prettier prima del commit
- **Verificare** formattazione con `npm run format:check`
- **Conoscere** i casi speciali e le soluzioni
- **Mantenere** coerenza in tutto il progetto

## 🎯 Perché Questa Scelta?

### **✅ Vantaggi:**
1. **Stile moderno** allineato con React 19 + Vite
2. **Codice più pulito** e leggibile
3. **Meno verboso** e più veloce da scrivere
4. **Standard** di molti framework moderni

### **⚠️ Considerazioni:**
1. **Team futuri** devono conoscere le regole
2. **Possibili ambiguità** (risolvibili con conoscenza)
3. **Standard diverso** da molte aziende tradizionali

## 🔄 Migrazione e Onboarding

### **Per nuovi sviluppatori:**
1. **Leggere** questa guida completamente
2. **Installare** Prettier extension nell'editor
3. **Configurare** editor per auto-format
4. **Testare** con `npm run format:check`
5. **Familiarizzare** con i casi speciali

### **Per team esistenti:**
1. **Rivedere** codice esistente
2. **Applicare** nuovo stile gradualmente
3. **Aggiornare** documentazione interna
4. **Formare** team sulle nuove regole

---

**📝 Nota:** Questa guida è viva e deve essere aggiornata quando vengono modificate le regole o aggiunti nuovi strumenti al progetto.


