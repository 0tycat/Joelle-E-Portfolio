# Docker & Backend Setup

## Prerequisites
- Docker Desktop installed and running
- `.env` file in project root with:
  ```
  SUPABASE_URL=your_url
  SUPABASE_SERVICE_KEY=your_service_key
  SUPABASE_ANON_KEY=your_anon_key
  ```

## Run Backend with Docker

**Build and start all services:**
```pwsh
docker compose up --build
```

This will start:
- Composite server at `http://127.0.0.1:8000`
- Auth server at `http://127.0.0.1:5005`

Both services are in one container but run in parallel.

**Stop services:**
```pwsh
docker compose down
```

**View logs:**
```pwsh
docker compose logs -f
```

## Run Frontend (Separate Terminal)

```pwsh
cd frontend
npm run dev
```

Visit `http://localhost:5173`

## Architecture

```
┌─────────────┐
│  Frontend   │ (Vue 3, npm run dev)
│  :5173      │
└──────┬──────┘
       │ HTTP calls
       ▼
┌─────────────────┐
│ Docker Backend  │
├─────────────────┤
│ Composite :8000 │ (/api/*)
│ Auth :5005      │ (/auth/*)
└─────────────────┘
       │
       ▼
  Supabase DB
```

## First Time Setup

1. Clone `.env.example` to `.env` and fill in Supabase keys
2. Run: `docker compose up --build`
3. In another terminal: `cd frontend && npm run dev`
4. Open `http://localhost:5173`
