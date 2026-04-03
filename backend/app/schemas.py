from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List
from datetime import datetime


def _validar_nombre(valor: Optional[str], campo: str) -> Optional[str]:
    if valor is None:
        return valor
    valor = valor.strip()
    if len(valor) < 3:
        raise ValueError(f"{campo}: mínimo 3 caracteres")

    import re
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+", valor):
        raise ValueError(f"{campo}: solo se permiten letras y espacios")
    return valor


def _validar_direccion(valor: Optional[str], campo: str) -> Optional[str]:
    if valor is None:
        return valor
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{campo}: campo obligatorio")

    import re
    if not re.search(r"\d", valor):
        raise ValueError(f"{campo}: debe incluir un número")
    return valor


def _validar_telefono(valor: Optional[str]) -> Optional[str]:
    if valor is None:
        return valor
    valor = valor.strip()
    if not valor:
        return None

    import re
    if not re.fullmatch(r"\+54 9 \d{2,4} \d{3,4}-\d{4}", valor):
        raise ValueError("tel_destinatario: formato argentino requerido (+54 9 XX XXXX-XXXX)")
    return valor


def _validar_tipo_peso(tipo_paquete: Optional[str], peso_kg: Optional[float]) -> None:
    if peso_kg is None:
        return

    if tipo_paquete == "Sobre" and peso_kg > 2:
        raise ValueError("Un Sobre no puede superar 2 kg")

    if tipo_paquete == "Pallet" and peso_kg < 50:
        raise ValueError("Un Pallet requiere mínimo 50 kg")


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

    @field_validator("remitente", "destinatario")
    @classmethod
    def validar_nombres(cls, value, info):
        return _validar_nombre(value, info.field_name)

    @field_validator("origen_direccion", "destino_direccion")
    @classmethod
    def validar_direcciones(cls, value, info):
        return _validar_direccion(value, info.field_name)

    @field_validator("tel_destinatario")
    @classmethod
    def validar_telefono(cls, value):
        return _validar_telefono(value)

    @model_validator(mode="after")
    def validar_peso_tipo(self):
        _validar_tipo_peso(self.tipo_paquete, self.peso_kg)
        return self


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

    @field_validator("remitente", "destinatario")
    @classmethod
    def validar_nombres(cls, value, info):
        return _validar_nombre(value, info.field_name)

    @field_validator("origen_direccion", "destino_direccion")
    @classmethod
    def validar_direcciones(cls, value, info):
        return _validar_direccion(value, info.field_name)

    @field_validator("tel_destinatario")
    @classmethod
    def validar_telefono(cls, value):
        return _validar_telefono(value)

    @model_validator(mode="after")
    def validar_peso_tipo(self):
        _validar_tipo_peso(self.tipo_paquete, self.peso_kg)
        return self

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
