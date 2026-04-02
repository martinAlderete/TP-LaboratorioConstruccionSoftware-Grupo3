"""
backend/app/routers/prediccion.py
Endpoint REST de predicción de demoras — LogiTrack
TP Laboratorio de Construcción de Software — UNGS 1C2026
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.ml.predictor import predecir as ml_predecir

router = APIRouter()


class PrediccionRequest(BaseModel):
    origen:       str   = Field(..., example="Córdoba")
    destino:      str   = Field(..., example="Buenos Aires")
    distancia_km: float = Field(..., gt=0, example=820.0)
    peso_kg:      float = Field(..., gt=0, example=12.5)
    tipo_paquete: str   = Field(..., example="Caja pequeña")


class PrediccionResponse(BaseModel):
    demorado:     bool
    probabilidad: float


@router.post(
    "/",
    response_model=PrediccionResponse,
    summary="Predice si un envío tendrá demora",
)
def predecir_demora(req: PrediccionRequest):
    """
    Recibe los datos de un envío y devuelve la predicción del modelo GaussianNB.

    - **demorado**: `true` si el modelo predice demora
    - **probabilidad**: probabilidad de demora entre 0.0 y 1.0
    """
    return ml_predecir(
        origen=req.origen,
        destino=req.destino,
        distancia_km=req.distancia_km,
        peso_kg=req.peso_kg,
        tipo_paquete=req.tipo_paquete,
    )
