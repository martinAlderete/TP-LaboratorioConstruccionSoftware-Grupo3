# ⬡ LogiTrack — MVP 1C2026

Sistema Federal de Gestión de Logística y Distribución  
**Materia:** Laboratorio de Construcción de Software — UNGS  
**Equipo:** Alderete · Gottig · Segovia

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML / CSS / JavaScript (SPA) |
| Backend | Python 3.11 + FastAPI |
| Base de datos | PostgreSQL (Railway) / SQLite (local) |
| Deploy backend | Railway |
| Deploy frontend | Netlify |
| CI | GitHub Actions |

---

## Estructura del Repositorio

```
logitrack/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI — backend + frontend
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app + CORS + startup
│   │   ├── database.py         # SQLAlchemy — PostgreSQL / SQLite
│   │   ├── models.py           # Tablas: Envio, EventoTracking, Usuario, SolicitudARCO
│   │   ├── schemas.py          # Schemas Pydantic (request/response)
│   │   ├── seed.py             # Datos iniciales (4 envíos + 5 usuarios)
│   │   └── routers/
│   │       ├── envios.py       # CRUD envíos, búsqueda, métricas, bulk
│   │       ├── usuarios.py     # Login, CRUD usuarios, toggle activo
│   │       └── arco.py         # Solicitudes Ley 25.326
│   ├── tests/
│   │   └── test_api.py         # 25+ tests de integración con TestClient
│   ├── requirements.txt
│   ├── Procfile                # Para Railway
│   └── railway.toml
├── frontend/
│   ├── index.html              # SPA conectada a la API real
│   ├── env.js                  # URL del backend (editar antes de deployar)
│   └── netlify.toml
├── docs/
│   └── dataset/
│       └── envios_historicos.csv
├── src/
│   └── ia/
│       └── prediccion_demoras.py
├── tests/
│   └── test_basic.js           # Tests de lógica JS
├── README.md
├── CONTRIBUTING.md
└── package.json
```

---

## Cómo correr localmente

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# API disponible en http://localhost:8000
# Docs interactivas en http://localhost:8000/docs
```

La primera vez que arranca, crea la BD SQLite (`logitrack.db`) y carga los datos semilla automáticamente.

### Frontend

Abrí `frontend/index.html` directamente en el navegador. El `env.js` ya apunta a `http://localhost:8000`.

---

## Deploy en Railway (Backend + PostgreSQL)

1. Crear proyecto en [railway.app](https://railway.app)
2. Agregar servicio **PostgreSQL** → Railway te da la variable `DATABASE_URL` automáticamente
3. Agregar servicio **GitHub Repo** → apuntar a la carpeta `/backend`
4. Railway detecta el `Procfile` y `railway.toml` automáticamente
5. En **Variables**, verificar que `DATABASE_URL` esté presente (Railway lo inyecta solo)
6. Copiar la URL pública del backend (ej: `https://logitrack-backend-production.up.railway.app`)

## Deploy en Netlify (Frontend)

1. Editar `frontend/env.js` y reemplazar la URL con la de Railway:
   ```js
   window.LOGITRACK_API_URL = 'https://TU-BACKEND.up.railway.app';
   ```
2. Hacer commit y push
3. En [netlify.com](https://netlify.com) → New site from Git → carpeta `frontend/`
4. Netlify detecta el `netlify.toml` automáticamente

---

## Usuarios de demo

| Username | Password | Rol |
|----------|----------|-----|
| `adm.sistema` | `adm1234` | Administrador |
| `sup.montero` | `sup1234` | Supervisor |
| `op.gonzalez` | `op1234` | Operador |
| `op.ramirez` | `op1234` | Operador |
| `op.garcia` | `op1234` | Operador (inactivo) |

---

## Endpoints principales de la API

```
GET    /api/envios                  Listado paginado
GET    /api/envios/metricas         Conteos por estado
GET    /api/envios/search?q=&estado= Búsqueda
GET    /api/envios/{tracking_id}    Detalle con historial
POST   /api/envios                  Alta de envío
PATCH  /api/envios/{id}/estado      Cambio de estado (Supervisor)
POST   /api/envios/bulk             Carga por lote (hasta 500)

POST   /api/usuarios/login          Autenticación
GET    /api/usuarios                Listado
POST   /api/usuarios                Crear usuario
PATCH  /api/usuarios/{username}/activo  Activar/desactivar

POST   /api/arco                    Solicitud Ley 25.326
GET    /api/arco                    Listar solicitudes
```

Documentación interactiva completa: `http://localhost:8000/docs`

---

## Tests

```bash
# Tests de API (backend)
cd backend
pytest tests/test_api.py -v

# Tests de lógica JS (frontend)
npm test
```

---

## CI/CD

El pipeline de GitHub Actions ejecuta automáticamente en cada push a `main`:
- **Backend**: instala dependencias Python y corre `pytest`
- **Frontend**: instala Node, corre ESLint y los tests JS básicos
