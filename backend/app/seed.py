from app.database import SessionLocal
from app import models
from datetime import datetime


def cargar_datos_iniciales():
    db = SessionLocal()
    try:
        # Solo cargar si la BD está vacía
        if db.query(models.Usuario).count() > 0:
            return

        usuarios = [
            models.Usuario(username="adm.sistema",  nombre="Admin Sistema",      password_hash="adm1234",  rol="Administrador", activo=True),
            models.Usuario(username="sup.montero",  nombre="Juan Montero",        password_hash="sup1234",  rol="Supervisor",     activo=True),
            models.Usuario(username="op.gonzalez",  nombre="María González",      password_hash="op1234",   rol="Operador",       activo=True),
            models.Usuario(username="op.ramirez",   nombre="Carlos Ramírez",      password_hash="op1234",   rol="Operador",       activo=True),
            models.Usuario(username="op.garcia",    nombre="Laura García",         password_hash="op1234",   rol="Operador",       activo=False),
        ]
        db.add_all(usuarios)
        db.flush()

        # Envío 1 — En Tránsito
        e1 = models.Envio(
            tracking_id="LT-2026-0001",
            remitente="Distribuidora Palermo S.A.",
            destinatario="Carlos Romero",
            origen_provincia="CABA",
            origen_ciudad="Buenos Aires",
            origen_direccion="Av. Corrientes 1234",
            destino_provincia="Córdoba",
            destino_ciudad="Córdoba",
            destino_direccion="Av. Colón 567",
            tel_destinatario="+54 9 351 555-0101",
            tipo_paquete="Caja estándar",
            peso_kg=12.5,
            observaciones="Frágil, manejar con cuidado",
            estado="En Tránsito",
            fecha_creacion=datetime(2026, 3, 15, 9, 12),
            creado_por="op.gonzalez",
        )
        db.add(e1)
        db.flush()
        db.add_all([
            models.EventoTracking(tracking_id="LT-2026-0001", estado_anterior=None, estado_nuevo="Creado", timestamp=datetime(2026, 3, 15, 9, 12), usuario="op.gonzalez"),
            models.EventoTracking(tracking_id="LT-2026-0001", estado_anterior="Creado", estado_nuevo="En Preparación", timestamp=datetime(2026, 3, 15, 10, 30), usuario="sup.montero"),
            models.EventoTracking(tracking_id="LT-2026-0001", estado_anterior="En Preparación", estado_nuevo="En Tránsito", timestamp=datetime(2026, 3, 16, 8, 0), usuario="sup.montero"),
        ])

        # Envío 2 — Entregado
        e2 = models.Envio(
            tracking_id="LT-2026-0002",
            remitente="Logística Sur SRL",
            destinatario="Ana Martínez",
            origen_provincia="Buenos Aires",
            origen_ciudad="Mar del Plata",
            origen_direccion="San Martín 890",
            destino_provincia="Santa Fe",
            destino_ciudad="Rosario",
            destino_direccion="Pellegrini 234",
            tel_destinatario="+54 9 341 555-0202",
            tipo_paquete="Sobre",
            peso_kg=0.3,
            estado="Entregado",
            fecha_creacion=datetime(2026, 3, 14, 8, 0),
            creado_por="op.ramirez",
        )
        db.add(e2)
        db.flush()
        db.add_all([
            models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior=None, estado_nuevo="Creado", timestamp=datetime(2026, 3, 14, 8, 0), usuario="op.ramirez"),
            models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior="Creado", estado_nuevo="En Preparación", timestamp=datetime(2026, 3, 14, 9, 15), usuario="sup.montero"),
            models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior="En Preparación", estado_nuevo="En Tránsito", timestamp=datetime(2026, 3, 14, 14, 0), usuario="sup.montero"),
            models.EventoTracking(tracking_id="LT-2026-0002", estado_anterior="En Tránsito", estado_nuevo="Entregado", timestamp=datetime(2026, 3, 15, 11, 20), usuario="sup.montero"),
        ])

        # Envío 3 — En Preparación
        e3 = models.Envio(
            tracking_id="LT-2026-0003",
            remitente="Grupo Norte Express",
            destinatario="Municipalidad de Salta",
            origen_provincia="Salta",
            origen_ciudad="Salta",
            origen_direccion="Caseros 123",
            destino_provincia="Tucumán",
            destino_ciudad="San Miguel de Tucumán",
            destino_direccion="24 de Septiembre 450",
            tel_destinatario="+54 387 421-0000",
            tipo_paquete="Pallet",
            peso_kg=80.0,
            observaciones="Requiere grúa",
            estado="En Preparación",
            fecha_creacion=datetime(2026, 3, 17, 7, 45),
            creado_por="op.garcia",
        )
        db.add(e3)
        db.flush()
        db.add_all([
            models.EventoTracking(tracking_id="LT-2026-0003", estado_anterior=None, estado_nuevo="Creado", timestamp=datetime(2026, 3, 17, 7, 45), usuario="op.garcia"),
            models.EventoTracking(tracking_id="LT-2026-0003", estado_anterior="Creado", estado_nuevo="En Preparación", timestamp=datetime(2026, 3, 17, 9, 0), usuario="sup.montero"),
        ])

        # Envío 4 — Creado
        e4 = models.Envio(
            tracking_id="LT-2026-0004",
            remitente="TechStore Argentina",
            destinatario="Pedro Vidal",
            origen_provincia="CABA",
            origen_ciudad="Buenos Aires",
            origen_direccion="Florida 560",
            destino_provincia="Mendoza",
            destino_ciudad="Mendoza",
            destino_direccion="Aristides Villanueva 789",
            tel_destinatario="+54 9 261 555-0303",
            tipo_paquete="Frágil",
            peso_kg=3.2,
            observaciones="Equipo electrónico",
            estado="Creado",
            fecha_creacion=datetime(2026, 3, 18, 14, 20),
            creado_por="op.gonzalez",
        )
        db.add(e4)
        db.flush()
        db.add(models.EventoTracking(tracking_id="LT-2026-0004", estado_anterior=None, estado_nuevo="Creado", timestamp=datetime(2026, 3, 18, 14, 20), usuario="op.gonzalez"))

        db.commit()
        print("✅ Datos iniciales cargados correctamente.")
    except Exception as e:
        db.rollback()
        print(f"⚠ Error al cargar datos iniciales: {e}")
    finally:
        db.close()
