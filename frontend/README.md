# Joelle E-Portfolio Frontend

## Setup

1. Install dependencies:
```pwsh
cd frontend
npm install
```

2. Configure environment (optional):
Create `frontend/.env` with:
```
VITE_API_URL=http://127.0.0.1:8000
VITE_AUTH_URL=http://127.0.0.1:5005
```

3. Run dev server:
```pwsh
npm run dev
```

Open `http://127.0.0.1:5173`.

## Pages
- Skills `/skills`
- Work Experience `/experience`
- Education `/education`
- Other Information `/other-information`
- Login `/login`

## Auth
- Login via `/login` calls backend auth and stores tokens.
- Sidebar shows Login/Logout button based on state.
