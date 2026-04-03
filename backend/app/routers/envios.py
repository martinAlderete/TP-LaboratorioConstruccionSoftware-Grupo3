import random
import string
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db
from app import models, schemas

router = APIRouter()

ESTADOS_ORDEN = ["Creado", "En Preparación", "En Tránsito", "Entregado"]

PROVINCIAS = ["Buenos Aires","CABA","Córdoba","Santa Fe","Mendoza","Tucumán","Salta","Neuquén","Entre Ríos","Misiones","Chaco","Corrientes","Santiago del Estero","San Juan","Jujuy","Río Negro","Formosa","Chubut","San Luis","Catamarca","La Rioja","La Pampa","Santa Cruz","Tierra del Fuego"]
CIUDADES = {"Buenos Aires":["La Plata","Mar del Plata","Bahía Blanca","Tandil","Quilmes"],"CABA":["Palermo","Belgrano","Recoleta","San Telmo","Caballito"],"Córdoba":["Córdoba","Villa María","Río Cuarto"],"Santa Fe":["Rosario","Santa Fe","Rafaela"],"Mendoza":["Mendoza","San Rafael","Godoy Cruz"],"Tucumán":["San Miguel de Tucumán","Yerba Buena"],"Salta":["Salta","San Lorenzo","Tartagal"],"Neuquén":["Neuquén","San Martín de los Andes"],"Entre Ríos":["Paraná","Concordia"],"Misiones":["Posadas","Oberá"],"Chaco":["Resistencia","Barranqueras"],"Corrientes":["Corrientes","Goya"],"Santiago del Estero":["Santiago del Estero","La Banda"],"San Juan":["San Juan","Rawson"],"Jujuy":["San Salvador de Jujuy","Palpalá"],"Río Negro":["Viedma","Bariloche","General Roca"],"Formosa":["Formosa","Clorinda"],"Chubut":["Rawson","Trelew","Comodoro Rivadavia"],"San Luis":["San Luis","Villa Mercedes"],"Catamarca":["San Fernando del Valle de Catamarca"],"La Rioja":["La Rioja","Chilecito"],"La Pampa":["Santa Rosa","General Pico"],"Santa Cruz":["Río Gallegos","Caleta Olivia"],"Tierra del Fuego":["Ushuaia","Río Grande"]}
CALLES = ["Av. San Martín","Av. Rivadavia","Belgrano","Mitre","Sarmiento","Av. Corrientes","25 de Mayo","9 de Julio","Urquiza","Moreno","Lavalle","Güemes"]
TIPOS = ["Caja estándar","Sobre","Pallet","Frágil","Refrigerado"]
REMITENTES = ["Distribuidora Palermo S.A.","Logística Sur SRL","Grupo Norte Express","TechStore Argentina","Farmacia del Pueblo","Librería Nacional","Electro Hogar","MegaDistribuciones","Patagonia Logistics","Envíos Rápidos CABA","Transportes Unión","Industrial del Norte","AgriPack SRL","Mercado Express"]
DESTINATARIOS = ["Carlos Romero","Ana Martínez","Pedro Vidal","Lucía Fernández","Jorge López","Marta Rodríguez","Diego Sánchez","Valentina García","Santiago Moreno","Camila Díaz","Matías Ruiz","Florencia Torres","Nicolás Pereyra","Julieta Álvarez","Tomás Castro","Mariana Giménez"]
OPERADORES = ["op.gonzalez","op.ramirez","op.garcia"]


def _next_tracking_id(db: Session) -> str:
    year = datetime.now().year
    prefix = f"LT-{year}-"
    last = db.query(models.Envio).filter(
        models.Envio.tracking_id.like(f"{prefix}%")
    ).order_by(models.Envio.tracking_id.desc()).first()
    num = 1
    if last:
        try:
            num = int(last.tracking_id.split("-")[-1]) + 1
        except ValueError:
            num = 1
    return f"{prefix}{str(num).zfill(4)}"


# ── Listado paginado ──────────────────────────────────────────────────────────

@router.get("", response_model=dict)
def listar_envios(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total = db.query(models.Envio).count()
    envios = (
        db.query(models.Envio)
        .order_by(models.Envio.fecha_creacion.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "items": [schemas.EnvioListItem.from_orm(e) for e in envios],
    }


# ── Métricas ──────────────────────────────────────────────────────────────────

@router.get("/metricas")
def metricas(db: Session = Depends(get_db)):
    total = db.query(models.Envio).count()
    por_estado = {
        row[0]: row[1]
        for row in db.query(models.Envio.estado, func.count()).group_by(models.Envio.estado).all()
    }
    return {
        "total": total,
        "creado": por_estado.get("Creado", 0),
        "en_preparacion": por_estado.get("En Preparación", 0),
        "en_transito": por_estado.get("En Tránsito", 0),
        "entregado": por_estado.get("Entregado", 0),
    }


# ── Búsqueda ──────────────────────────────────────────────────────────────────

@router.get("/search", response_model=list)
def buscar_envios(
    q: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Envio)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                models.Envio.tracking_id.ilike(like),
                models.Envio.destinatario.ilike(like),
                models.Envio.remitente.ilike(like),
            )
        )
    if estado:
        query = query.filter(models.Envio.estado == estado)
    envios = query.order_by(models.Envio.fecha_creacion.desc()).limit(100).all()
    return [schemas.EnvioListItem.from_orm(e) for e in envios]


# ── Detalle ───────────────────────────────────────────────────────────────────

@router.get("/{tracking_id}", response_model=schemas.EnvioOut)
def detalle_envio(tracking_id: str, db: Session = Depends(get_db)):
    envio = db.query(models.Envio).filter(models.Envio.tracking_id == tracking_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    return envio


# ── Alta ──────────────────────────────────────────────────────────────────────

@router.post("", response_model=schemas.EnvioOut, status_code=201)
def crear_envio(
    data: schemas.EnvioCreate,
    usuario: str = Query("sistema"),
    db: Session = Depends(get_db)
):
    tracking_id = _next_tracking_id(db)
    envio = models.Envio(
        tracking_id=tracking_id,
        remitente=data.remitente,
        destinatario=data.destinatario,
        origen_provincia=data.origen_provincia,
        origen_ciudad=data.origen_ciudad,
        origen_direccion=data.origen_direccion,
        destino_provincia=data.destino_provincia,
        destino_ciudad=data.destino_ciudad,
        destino_direccion=data.destino_direccion,
        tel_destinatario=data.tel_destinatario,
        tipo_paquete=data.tipo_paquete or "Caja estándar",
        peso_kg=data.peso_kg,
        observaciones=data.observaciones,
        estado="Creado",
        creado_por=usuario,
    )
    db.add(envio)
    db.flush()
    evento = models.EventoTracking(
        tracking_id=tracking_id,
        estado_anterior=None,
        estado_nuevo="Creado",
        usuario=usuario,
    )
    db.add(evento)
    db.commit()
    db.refresh(envio)
    return envio


# ── Cambio de estado ──────────────────────────────────────────────────────────

@router.patch("/{tracking_id}/estado", response_model=schemas.EnvioOut)
def cambiar_estado(
    tracking_id: str,
    data: schemas.CambioEstadoRequest,
    db: Session = Depends(get_db)
):
    envio = db.query(models.Envio).filter(models.Envio.tracking_id == tracking_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    estado_actual_idx = ESTADOS_ORDEN.index(envio.estado) if envio.estado in ESTADOS_ORDEN else -1
    nuevo_idx = ESTADOS_ORDEN.index(data.nuevo_estado) if data.nuevo_estado in ESTADOS_ORDEN else -1
    if nuevo_idx != estado_actual_idx + 1:
        raise HTTPException(status_code=400, detail=f"Transición inválida: {envio.estado} → {data.nuevo_estado}")
    estado_anterior = envio.estado
    envio.estado = data.nuevo_estado
    evento = models.EventoTracking(
        tracking_id=tracking_id,
        estado_anterior=estado_anterior,
        estado_nuevo=data.nuevo_estado,
        usuario=data.usuario,
        observaciones=data.observaciones,
    )
    db.add(evento)
    db.commit()
    db.refresh(envio)
    return envio


# ── Editar envío (solo estado Creado) ─────────────────────────────────────────

@router.put("/{tracking_id}", response_model=schemas.EnvioOut)
def editar_envio(
    tracking_id: str,
    data: schemas.EnvioUpdate,
    usuario: str = Query("sistema"),
    db: Session = Depends(get_db)
):
    envio = db.query(models.Envio).filter(models.Envio.tracking_id == tracking_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    if envio.estado != "Creado":
        raise HTTPException(status_code=400, detail="Solo se pueden editar envíos en estado 'Creado'")
    for field, value in data.dict(exclude_none=True).items():
        setattr(envio, field, value)
    evento = models.EventoTracking(
        tracking_id=tracking_id,
        estado_anterior="Creado",
        estado_nuevo="Creado",
        usuario=usuario,
        observaciones="Datos del envío editados",
    )
    db.add(evento)
    db.commit()
    db.refresh(envio)
    return envio


# ── Eliminar envío ────────────────────────────────────────────────────────────

@router.delete("/{tracking_id}", status_code=204)
def eliminar_envio(
    tracking_id: str,
    db: Session = Depends(get_db)
):
    envio = db.query(models.Envio).filter(models.Envio.tracking_id == tracking_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    db.query(models.EventoTracking).filter(
        models.EventoTracking.tracking_id == tracking_id
    ).delete()
    db.delete(envio)
    db.commit()


# ── Carga por lote ────────────────────────────────────────────────────────────

@router.post("/bulk", status_code=201)
def carga_lote(data: schemas.BulkRequest, db: Session = Depends(get_db)):
    cantidad = min(max(data.cantidad, 1), 500)
    creados = []
    for _ in range(cantidad):
        prov_orig = random.choice(PROVINCIAS)
        prov_dest = random.choice(PROVINCIAS)
        ciudad_orig = random.choice(CIUDADES.get(prov_orig, ["Centro"]))
        ciudad_dest = random.choice(CIUDADES.get(prov_dest, ["Centro"]))
        calle_orig = random.choice(CALLES) + " " + str(random.randint(100, 9999))
        calle_dest = random.choice(CALLES) + " " + str(random.randint(100, 9999))
        estado_idx = random.randint(0, 3)
        estado = ESTADOS_ORDEN[estado_idx]
        tracking_id = _next_tracking_id(db)
        envio = models.Envio(
            tracking_id=tracking_id,
            remitente=random.choice(REMITENTES),
            destinatario=random.choice(DESTINATARIOS),
            origen_provincia=prov_orig,
            origen_ciudad=ciudad_orig,
            origen_direccion=calle_orig,
            destino_provincia=prov_dest,
            destino_ciudad=ciudad_dest,
            destino_direccion=calle_dest,
            tipo_paquete=random.choice(TIPOS),
            peso_kg=round(random.uniform(0.1, 50.0), 1),
            estado=estado,
            creado_por=random.choice(OPERADORES),
        )
        db.add(envio)
        db.flush()
        for i in range(estado_idx + 1):
            db.add(models.EventoTracking(
                tracking_id=tracking_id,
                estado_anterior=ESTADOS_ORDEN[i - 1] if i > 0 else None,
                estado_nuevo=ESTADOS_ORDEN[i],
                usuario=random.choice(OPERADORES) if i == 0 else "sup.montero",
            ))
        creados.append(tracking_id)
    db.commit()
    return {"creados": len(creados), "mensaje": f"Se generaron {len(creados)} envíos correctamente."}
