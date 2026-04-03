from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class RolEnum(str, enum.Enum):
    Operador = "Operador"
    Supervisor = "Supervisor"
    Administrador = "Administrador"


class EstadoEnum(str, enum.Enum):
    Creado = "Creado"
    En_Preparacion = "En Preparación"
    En_Transito = "En Tránsito"
    Entregado = "Entregado"


class TipoPaqueteEnum(str, enum.Enum):
    Caja_estandar = "Caja estándar"
    Sobre = "Sobre"
    Pallet = "Pallet"
    Fragil = "Frágil"
    Refrigerado = "Refrigerado"


class Usuario(Base):
    __tablename__ = "usuarios"

    username = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="Operador")
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    envios_creados = relationship("Envio", back_populates="creador")
    eventos = relationship("EventoTracking", back_populates="usuario_obj")


class Envio(Base):
    __tablename__ = "envios"

    tracking_id = Column(String, primary_key=True, index=True)
    remitente = Column(String, nullable=False)
    destinatario = Column(String, nullable=False)
    origen_provincia = Column(String, nullable=False)
    origen_ciudad = Column(String, nullable=False)
    origen_direccion = Column(String, nullable=False)
    destino_provincia = Column(String, nullable=False)
    destino_ciudad = Column(String, nullable=False)
    destino_direccion = Column(String, nullable=False)
    tel_destinatario = Column(String, nullable=True)
    tipo_paquete = Column(String, nullable=False, default="Caja estándar")
    peso_kg = Column(Float, nullable=True)
    observaciones = Column(Text, nullable=True)
    estado = Column(String, nullable=False, default="Creado")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    creado_por = Column(String, ForeignKey("usuarios.username"), nullable=True)

    creador = relationship("Usuario", back_populates="envios_creados")
 
    historial = relationship("EventoTracking", back_populates="envio", order_by="EventoTracking.timestamp", cascade="all, delete-orphan")


class EventoTracking(Base):
    __tablename__ = "eventos_tracking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_id = Column(String, ForeignKey("envios.tracking_id"), nullable=False)
    estado_anterior = Column(String, nullable=True)
    estado_nuevo = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    usuario = Column(String, ForeignKey("usuarios.username"), nullable=True)
    observaciones = Column(Text, nullable=True)

    envio = relationship("Envio", back_populates="historial")
    usuario_obj = relationship("Usuario", back_populates="eventos")


class SolicitudARCO(Base):
    __tablename__ = "solicitudes_arco"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    tracking_relacionado = Column(String, nullable=True)
    descripcion = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    resuelta = Column(Boolean, default=False)
