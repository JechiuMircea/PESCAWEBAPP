# Pesca WebApp - Frontend React + TypeScript + Vite

**Applicazione per identificazione e gestione pesci con design responsive completo.**

## 🎯 Caratteristiche Principali

- **React 19** con TypeScript per type safety
- **Vite** per build veloce e HMR
- **Design Responsive** per mobile, tablet e desktop
- **Componenti UI** modulari e riutilizzabili
- **ESLint + Prettier** per code quality

## 📱 Responsive Web Design

### Breakpoints Implementati:
- **Mobile**: `max-width: 480px`
- **Tablet**: `max-width: 768px` 
- **Desktop**: `min-width: 1024px`

### Componenti Responsive:
- **Header**: Adattivo con menu mobile
- **Navigation**: Collapsible su dispositivi piccoli
- **Dashboard**: Layout flessibile per tutti gli schermi
- **Catalogo**: Grid responsive per specie
- **Identificatore**: Form ottimizzato per touch

## 🚀 Script Disponibili

- `npm run dev` - Server sviluppo con HMR
- `npm run build` - Build produzione ottimizzato
- `npm run preview` - Preview build produzione
- `npm run quality` - Controllo qualità codice
- `npm run test` - Testing con Jest

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      ...tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      ...tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
