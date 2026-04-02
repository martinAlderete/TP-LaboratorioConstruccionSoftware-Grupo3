from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("", response_model=schemas.ARCOOut, status_code=201)
def crear_solicitud_arco(data: schemas.ARCOCreate, db: Session = Depends(get_db)):
    solicitud = models.SolicitudARCO(
        nombre=data.nombre,
        email=data.email,
        tipo=data.tipo,
        tracking_relacionado=data.tracking_relacionado,
        descripcion=data.descripcion,
    )
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)
    return solicitud


@router.get("", response_model=list)
def listar_solicitudes(db: Session = Depends(get_db)):
    solicitudes = db.query(models.SolicitudARCO).order_by(models.SolicitudARCO.fecha.desc()).all()
    return [schemas.ARCOOut.from_orm(s) for s in solicitudes]
