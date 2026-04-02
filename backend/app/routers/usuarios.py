from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/login", response_model=schemas.LoginResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == data.username).first()
    if not usuario or usuario.password_hash != data.password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos.")
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Tu cuenta está desactivada. Contactá al administrador.")
    initials = "".join(w[0] for w in usuario.nombre.split()[:2]).upper()
    return schemas.LoginResponse(
        username=usuario.username,
        nombre=usuario.nombre,
        rol=usuario.rol,
        initials=initials,
    )


@router.get("", response_model=list)
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return [schemas.UsuarioOut.from_orm(u) for u in usuarios]


@router.post("", response_model=schemas.UsuarioOut, status_code=201)
def crear_usuario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.username == data.username).first()
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")
    usuario = models.Usuario(
        username=data.username,
        nombre=data.nombre,
        password_hash=data.password or "password123",
        rol=data.rol,
        activo=data.activo if data.activo is not None else True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.patch("/{username}/activo", response_model=schemas.UsuarioOut)
def toggle_activo(username: str, data: schemas.ToggleActivoRequest, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == username).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    usuario.activo = data.activo
    db.commit()
    db.refresh(usuario)
    return usuario
