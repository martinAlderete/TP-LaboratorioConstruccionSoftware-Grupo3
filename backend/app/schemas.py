from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username: str
    nombre: str
    rol: str
    initials: str


# ── EventoTracking ────────────────────────────────────────────────────────────

class EventoTrackingOut(BaseModel):
    id: int
    estado_anterior: Optional[str]
    estado_nuevo: str
    timestamp: datetime
    usuario: Optional[str]
    observaciones: Optional[str]

    class Config:
        from_attributes = True


# ── Envío ─────────────────────────────────────────────────────────────────────

class EnvioCreate(BaseModel):
    remitente: str
    destinatario: str
    origen_provincia: str
    origen_ciudad: str
    origen_direccion: str
    destino_provincia: str
    destino_ciudad: str
    destino_direccion: str
    tel_destinatario: Optional[str] = None
    tipo_paquete: Optional[str] = "Caja estándar"
    peso_kg: Optional[float] = None
    observaciones: Optional[str] = None


class EnvioUpdate(BaseModel):
    remitente: Optional[str] = None
    destinatario: Optional[str] = None
    origen_provincia: Optional[str] = None
    origen_ciudad: Optional[str] = None
    origen_direccion: Optional[str] = None
    destino_provincia: Optional[str] = None
    destino_ciudad: Optional[str] = None
    destino_direccion: Optional[str] = None
    tel_destinatario: Optional[str] = None
    tipo_paquete: Optional[str] = None
    peso_kg: Optional[float] = None
    observaciones: Optional[str] = None


class EnvioOut(BaseModel):
    tracking_id: str
    remitente: str
    destinatario: str
    origen_provincia: str
    origen_ciudad: str
    origen_direccion: str
    destino_provincia: str
    destino_ciudad: str
    destino_direccion: str
    tel_destinatario: Optional[str]
    tipo_paquete: str
    peso_kg: Optional[float]
    observaciones: Optional[str]
    estado: str
    fecha_creacion: datetime
    creado_por: Optional[str]
    historial: List[EventoTrackingOut] = []

    class Config:
        from_attributes = True


class EnvioListItem(BaseModel):
    tracking_id: str
    remitente: str
    destinatario: str
    destino_provincia: str
    destino_ciudad: str
    estado: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class CambioEstadoRequest(BaseModel):
    nuevo_estado: str
    usuario: str
    observaciones: Optional[str] = None


class BulkRequest(BaseModel):
    cantidad: int = 10


# ── Usuario ───────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    username: str
    nombre: str
    rol: str
    activo: Optional[bool] = True
    password: Optional[str] = "password123"


class UsuarioOut(BaseModel):
    username: str
    nombre: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True


class ToggleActivoRequest(BaseModel):
    activo: bool


# ── ARCO ──────────────────────────────────────────────────────────────────────

class ARCOCreate(BaseModel):
    nombre: str
    email: str
    tipo: str
    tracking_relacionado: Optional[str] = None
    descripcion: str


class ARCOOut(BaseModel):
    id: int
    nombre: str
    email: str
    tipo: str
    tracking_relacionado: Optional[str]
    descripcion: str
    fecha: datetime
    resuelta: bool

    class Config:
        from_attributes = True
