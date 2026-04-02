"""
tests/test_api.py
Tests de integración para la API de LogiTrack — Semana 4
Ejecutar con: pytest tests/test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# BD en memoria para tests
TEST_DATABASE_URL = "sqlite:///./test_logitrack.db"
engine_test = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    # Cargar seed usando la sesión de test
    from app import models
    from datetime import datetime
    db = TestingSession()
    try:
        if db.query(models.Usuario).count() == 0:
            usuarios = [
                models.Usuario(username="adm.sistema", nombre="Admin Sistema",   password_hash="adm1234", rol="Administrador", activo=True),
                models.Usuario(username="sup.montero", nombre="Juan Montero",    password_hash="sup1234", rol="Supervisor",     activo=True),
                models.Usuario(username="op.gonzalez", nombre="María González",  password_hash="op1234",  rol="Operador",       activo=True),
                models.Usuario(username="op.ramirez",  nombre="Carlos Ramírez",  password_hash="op1234",  rol="Operador",       activo=True),
                models.Usuario(username="op.garcia",   nombre="Laura García",    password_hash="op1234",  rol="Operador",       activo=False),
            ]
            db.add_all(usuarios)
            db.flush()
            e1 = models.Envio(tracking_id="LT-2026-0001", remitente="Distribuidora Palermo S.A.", destinatario="Carlos Romero", origen_provincia="CABA", origen_ciudad="Buenos Aires", origen_direccion="Av. Corrientes 1234", destino_provincia="Córdoba", destino_ciudad="Córdoba", destino_direccion="Av. Colón 567", tipo_paquete="Caja estándar", peso_kg=12.5, estado="En Tránsito", creado_por="op.gonzalez", fecha_creacion=datetime(2026,3,15,9,12))
            e2 = models.Envio(tracking_id="LT-2026-0002", remitente="Logística Sur SRL", destinatario="Ana Martínez", origen_provincia="Buenos Aires", origen_ciudad="Mar del Plata", origen_direccion="San Martín 890", destino_provincia="Santa Fe", destino_ciudad="Rosario", destino_direccion="Pellegrini 234", tipo_paquete="Sobre", peso_kg=0.3, estado="Entregado", creado_por="op.ramirez", fecha_creacion=datetime(2026,3,14,8,0))
            e3 = models.Envio(tracking_id="LT-2026-0003", remitente="Grupo Norte Express", destinatario="Municipalidad de Salta", origen_provincia="Salta", origen_ciudad="Salta", origen_direccion="Caseros 123", destino_provincia="Tucumán", destino_ciudad="San Miguel de Tucumán", destino_direccion="24 de Septiembre 450", tipo_paquete="Pallet", peso_kg=80.0, estado="En Preparación", creado_por="op.garcia", fecha_creacion=datetime(2026,3,17,7,45))
            e4 = models.Envio(tracking_id="LT-2026-0004", remitente="TechStore Argentina", destinatario="Pedro Vidal", origen_provincia="CABA", origen_ciudad="Buenos Aires", origen_direccion="Florida 560", destino_provincia="Mendoza", destino_ciudad="Mendoza", destino_direccion="Aristides Villanueva 789", tipo_paquete="Frágil", peso_kg=3.2, estado="Creado", creado_por="op.gonzalez", fecha_creacion=datetime(2026,3,18,14,20))
            db.add_all([e1, e2, e3, e4])
            db.flush()
            db.add_all([
                models.EventoTracking(tracking_id="LT-2026-0001", estado_anterior=None, estado_nuevo="Creado", usuario="op.gonzalez", timestamp=datetime(2026,3,15,9,12)),
                models.EventoTracking(tracking_id="LT-2026-0001", estado_anterior="Creado", estado_nuevo="En Preparación", usuario="sup.montero", timestamp=datetime(2026,3,15,10,30)),
                models.EventoTracking(tracking_id="LT-2026-0001", estado_anterior="En Preparación", estado_nuevo="En Tránsito", usuario="sup.montero", timestamp=datetime(2026,3,16,8,0)),
                models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior=None, estado_nuevo="Creado", usuario="op.ramirez", timestamp=datetime(2026,3,14,8,0)),
                models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior="Creado", estado_nuevo="En Preparación", usuario="sup.montero", timestamp=datetime(2026,3,14,9,15)),
                models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior="En Preparación", estado_nuevo="En Tránsito", usuario="sup.montero", timestamp=datetime(2026,3,14,14,0)),
                models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior="En Tránsito", estado_nuevo="Entregado", usuario="sup.montero", timestamp=datetime(2026,3,15,11,20)),
                models.EventoTracking(tracking_id="LT-2026-0003", estado_anterior=None, estado_nuevo="Creado", usuario="op.garcia", timestamp=datetime(2026,3,17,7,45)),
                models.EventoTracking(tracking_id="LT-2026-0003", estado_anterior="Creado", estado_nuevo="En Preparación", usuario="sup.montero", timestamp=datetime(2026,3,17,9,0)),
                models.EventoTracking(tracking_id="LT-2026-0004", estado_anterior=None, estado_nuevo="Creado", usuario="op.gonzalez", timestamp=datetime(2026,3,18,14,20)),
            ])
            db.commit()
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


client = TestClient(app)


# ── Health ────────────────────────────────────────────────────────────────────

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


# ── Auth ──────────────────────────────────────────────────────────────────────

def test_login_exitoso():
    res = client.post("/api/usuarios/login", json={"username": "op.gonzalez", "password": "op1234"})
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "op.gonzalez"
    assert data["rol"] == "Operador"


def test_login_password_incorrecta():
    res = client.post("/api/usuarios/login", json={"username": "op.gonzalez", "password": "wrongpass"})
    assert res.status_code == 401


def test_login_usuario_inexistente():
    res = client.post("/api/usuarios/login", json={"username": "noexiste", "password": "algo"})
    assert res.status_code == 401


def test_login_usuario_inactivo():
    res = client.post("/api/usuarios/login", json={"username": "op.garcia", "password": "op1234"})
    assert res.status_code == 403


# ── Envíos — Listado y Métricas ───────────────────────────────────────────────

def test_listar_envios():
    res = client.get("/api/envios")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert data["total"] >= 4


def test_metricas():
    res = client.get("/api/envios/metricas")
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert data["total"] >= 4
    assert "en_transito" in data
    assert "entregado" in data


# ── Envíos — Detalle ──────────────────────────────────────────────────────────

def test_detalle_envio_existente():
    res = client.get("/api/envios/LT-2026-0001")
    assert res.status_code == 200
    data = res.json()
    assert data["tracking_id"] == "LT-2026-0001"
    assert data["remitente"] == "Distribuidora Palermo S.A."
    assert len(data["historial"]) == 3


def test_detalle_envio_inexistente():
    res = client.get("/api/envios/LT-9999-9999")
    assert res.status_code == 404


# ── Envíos — Alta ─────────────────────────────────────────────────────────────

def test_crear_envio():
    payload = {
        "remitente": "Test Remitente S.A.",
        "destinatario": "Juan Test",
        "origen_provincia": "CABA",
        "origen_ciudad": "Buenos Aires",
        "origen_direccion": "Corrientes 1234",
        "destino_provincia": "Córdoba",
        "destino_ciudad": "Córdoba",
        "destino_direccion": "Colón 567",
        "tipo_paquete": "Caja estándar",
        "peso_kg": 5.0,
    }
    res = client.post("/api/envios?usuario=op.gonzalez", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["tracking_id"].startswith("LT-")
    assert data["estado"] == "Creado"
    assert data["creado_por"] == "op.gonzalez"
    assert len(data["historial"]) == 1
    assert data["historial"][0]["estado_nuevo"] == "Creado"


def test_tracking_id_unico():
    payload = {
        "remitente": "A", "destinatario": "B",
        "origen_provincia": "CABA", "origen_ciudad": "BA", "origen_direccion": "Calle 1",
        "destino_provincia": "Córdoba", "destino_ciudad": "Cba", "destino_direccion": "Calle 2",
    }
    res1 = client.post("/api/envios?usuario=op.gonzalez", json=payload)
    res2 = client.post("/api/envios?usuario=op.gonzalez", json=payload)
    assert res1.status_code == 201
    assert res2.status_code == 201
    assert res1.json()["tracking_id"] != res2.json()["tracking_id"]


# ── Envíos — Cambio de estado ─────────────────────────────────────────────────

def test_cambio_estado_valido():
    res = client.patch(
        "/api/envios/LT-2026-0004/estado",
        json={"nuevo_estado": "En Preparación", "usuario": "sup.montero", "observaciones": "Listo para despacho"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["estado"] == "En Preparación"
    eventos = data["historial"]
    ultimo = eventos[-1]
    assert ultimo["estado_nuevo"] == "En Preparación"
    assert ultimo["usuario"] == "sup.montero"
    assert ultimo["observaciones"] == "Listo para despacho"


def test_cambio_estado_invalido_salto():
    # LT-2026-0004 está en Creado, no puede saltar a Entregado
    res = client.patch(
        "/api/envios/LT-2026-0004/estado",
        json={"nuevo_estado": "Entregado", "usuario": "sup.montero"},
    )
    assert res.status_code == 400


def test_estado_entregado_es_final():
    # LT-2026-0002 ya está Entregado
    res = client.patch(
        "/api/envios/LT-2026-0002/estado",
        json={"nuevo_estado": "En Tránsito", "usuario": "sup.montero"},
    )
    assert res.status_code == 400


# ── Búsqueda ──────────────────────────────────────────────────────────────────

def test_busqueda_por_tracking_id():
    res = client.get("/api/envios/search?q=LT-2026-0001")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["tracking_id"] == "LT-2026-0001"


def test_busqueda_por_destinatario():
    res = client.get("/api/envios/search?q=Ana")
    assert res.status_code == 200
    data = res.json()
    assert any(e["destinatario"] == "Ana Martínez" for e in data)


def test_busqueda_sin_resultados():
    res = client.get("/api/envios/search?q=XYZ999NADA")
    assert res.status_code == 200
    assert res.json() == []


def test_filtro_por_estado():
    res = client.get("/api/envios/search?estado=Entregado")
    assert res.status_code == 200
    data = res.json()
    assert all(e["estado"] == "Entregado" for e in data)


# ── Carga por lote ────────────────────────────────────────────────────────────

def test_bulk_genera_envios():
    antes = client.get("/api/envios/metricas").json()["total"]
    res = client.post("/api/envios/bulk", json={"cantidad": 10})
    assert res.status_code == 201
    assert res.json()["creados"] == 10
    despues = client.get("/api/envios/metricas").json()["total"]
    assert despues == antes + 10


def test_bulk_limite_maximo():
    res = client.post("/api/envios/bulk", json={"cantidad": 999})
    assert res.status_code == 201
    assert res.json()["creados"] == 500  # capped at 500


# ── Usuarios ──────────────────────────────────────────────────────────────────

def test_listar_usuarios():
    res = client.get("/api/usuarios")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 5
    usernames = [u["username"] for u in data]
    assert "adm.sistema" in usernames
    assert "sup.montero" in usernames


def test_crear_usuario():
    res = client.post("/api/usuarios", json={
        "username": "op.nuevo",
        "nombre": "Nuevo Operador",
        "rol": "Operador",
        "activo": True,
        "password": "pass123",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "op.nuevo"
    assert data["rol"] == "Operador"


def test_crear_usuario_duplicado():
    res = client.post("/api/usuarios", json={
        "username": "op.gonzalez",
        "nombre": "Duplicado",
        "rol": "Operador",
    })
    assert res.status_code == 400


def test_toggle_usuario_activo():
    res = client.patch("/api/usuarios/op.gonzalez/activo", json={"activo": False})
    assert res.status_code == 200
    assert res.json()["activo"] == False
    # Reactivar
    res2 = client.patch("/api/usuarios/op.gonzalez/activo", json={"activo": True})
    assert res2.json()["activo"] == True


# ── ARCO ──────────────────────────────────────────────────────────────────────

def test_crear_solicitud_arco():
    res = client.post("/api/arco", json={
        "nombre": "Ana Martínez",
        "email": "ana@email.com",
        "tipo": "Acceso",
        "tracking_relacionado": "LT-2026-0002",
        "descripcion": "Quiero saber qué datos tiene el sistema sobre mí.",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["nombre"] == "Ana Martínez"
    assert data["tipo"] == "Acceso"
    assert data["resuelta"] == False


def test_listar_solicitudes_arco():
    client.post("/api/arco", json={
        "nombre": "Test", "email": "t@t.com",
        "tipo": "Supresión", "descripcion": "Eliminar datos",
    })
    res = client.get("/api/arco")
    assert res.status_code == 200
    assert len(res.json()) >= 1
