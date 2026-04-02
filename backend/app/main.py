from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import envios, usuarios, arco
from app import seed

app = FastAPI(
    title="LogiTrack API",
    description="Sistema Federal de Gestión de Logística y Distribución — UNGS 1C2026",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas y cargar datos iniciales al arrancar
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    seed.cargar_datos_iniciales()

app.include_router(envios.router, prefix="/api/envios", tags=["Envíos"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(arco.router, prefix="/api/arco", tags=["ARCO"])

@app.get("/")
def root():
    return {"message": "LogiTrack API activa", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
