# FastAPI-Auth0-Vue

A full-stack web application with Auth0 authentication, using FastAPI as the backend and Vue.js as the frontend.

## Tech Stack

### Backend
- Python
- FastAPI
- Auth0 (JWT validation)

### Frontend
- Vue.js
- Auth0 SPA SDK

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI application
│   ├── auth0.py         # Auth0 JWT verification
│   └── requirements.txt
└── frontend/
    ├── src/             # Vue.js source
    ├── auth_config.json # Auth0 configuration
    └── package.json
```

## Setup

### Backend

1. Create a `.env` file in the `backend/` directory:
   ```
   DOMAIN=your-sub-domain.auth0.com
   AUDIENCE=https://your-audience
   ```
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Frontend

1. Create `.env.development` in the `frontend/` directory:
   ```
   VUE_APP_ROOT_API=http://localhost:PORT_NUMBER
   ```
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   npm run serve
   ```
