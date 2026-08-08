# TOLLGATE — Agent Spend Policy Engine

## Run it

```
npm install
npm run dev
```

Then open the URL it prints (usually http://localhost:5173).

## Build for deployment

```
npm run build
```

This creates a `dist/` folder. Drag that folder into https://app.netlify.com/drop for an instant
public link, or push this whole folder to GitHub and import it on https://vercel.com.

## What's in here

- `src/App.jsx` — the entire app (dashboard, policy rules, x402 gate simulator, Algorand ledger,
  monitoring charts, audit log, architecture overview)
- `src/main.jsx` — mounts the app
- `src/index.css` — Tailwind entry
- `tailwind.config.js`, `postcss.config.js` — styling setup
- `vite.config.js` — build tool config
- `index.html` — page shell
- `package.json` — dependencies (react, recharts, lucide-react)
