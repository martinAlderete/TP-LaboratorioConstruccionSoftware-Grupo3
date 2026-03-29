# LogiTrack 🚚

**Sistema Federal de Gestión de Logística y Distribución**

[![CI](https://github.com/TU_USUARIO/logitrack/actions/workflows/ci.yml/badge.svg)](https://github.com/TU_USUARIO/logitrack/actions/workflows/ci.yml)

> Proyecto académico — Laboratorio de Construcción de Software · UNGS · 1C 2026  
> Integrantes: Martin Alderete · Juan Francisco Gottig · Juan Cruz Segovia

---

## Descripción

LogiTrack es un MVP de plataforma web para la gestión centralizada de envíos, orientada a operadores logísticos de mediana escala en Argentina. Permite registrar, seguir y gestionar envíos con tracking IDs automáticos, cambio de estados auditado, control de acceso por roles y predicción de demoras mediante IA.

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Frontend / Prototipo | HTML5, CSS3, JavaScript (Vanilla) |
| Mock API | JavaScript in-memory (datos embebidos) |
| Modelo IA | Python 3, scikit-learn |
| CI | GitHub Actions |
| Testing | Node.js + assert (built-in) |
| Linting | ESLint |

## Estructura del Proyecto

```
logitrack/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI (GitHub Actions)
├── docs/
│   └── dataset/
│       └── envios_historicos.csv   # Dataset simulado para modelo IA
├── src/
│   ├── index.html          # Prototipo navegable (SPA con Mock API)
│   └── ia/
│       └── prediccion_demoras.py   # Script de predicción de demoras
├── tests/
│   └── test_basic.js       # Tests básicos del sistema
├── README.md
├── CONTRIBUTING.md
└── package.json
```

## Instalación y Ejecución

### Requisitos previos
- Node.js v20 LTS o superior
- Python 3.10+ (solo para el modelo de IA)

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/logitrack.git
cd logitrack
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Ejecutar el prototipo

Abrir `src/index.html` directamente en el navegador (no requiere servidor).

### 4. Ejecutar los tests

```bash
npm test
```

### 5. Ejecutar el linter

```bash
npm run lint
```

### 6. Ejecutar el modelo de IA (independiente)

```bash
pip install scikit-learn pandas numpy
python src/ia/prediccion_demoras.py
```

## Funcionalidades del MVP (Semana 3)

- ✅ Alta de envío con tracking ID automático
- ✅ Listado paginado (20 ítems por página)
- ✅ Búsqueda por tracking ID, destinatario o remitente
- ✅ Cambio de estado con auditoría (rol Supervisor)
- ✅ Vista de detalle con historial de estados
- ✅ Login con control de acceso por roles (Operador / Supervisor)
- ✅ Carga masiva de envíos (hasta 500, para pruebas)
- ✅ Modelo de IA de predicción de demoras (ejecución independiente)
- ✅ Mock API con endpoints REST simulados

## Mock API — Endpoints simulados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/envios | Listado paginado |
| GET | /api/envios/:id | Detalle por tracking ID |
| POST | /api/envios | Alta de envío |
| PATCH | /api/envios/:id/estado | Cambio de estado |
| GET | /api/envios/search?q= | Búsqueda |
| POST | /api/envios/bulk | Carga masiva |

## Estrategia de Ramas

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para detalles completos.

| Rama | Uso |
|------|-----|
| `main` | Rama estable — solo recibe merges via PR aprobado |
| `feature/HU-XX` | Desarrollo de historias de usuario |
| `fix/descripcion` | Corrección de errores |
| `docs/descripcion` | Cambios en documentación |

## Matriz de Trazabilidad

| HU | Historia de Usuario | Casos de Prueba | Commit |
|----|---------------------|-----------------|--------|
| HU-01 | Registrar envío con tracking ID | CP-01 a CP-06 | `feat(envios): agregar alta de envío con tracking ID automático` |
| HU-02 | Buscar envíos | CP-17 a CP-24 | `feat(busqueda): agregar búsqueda por tracking ID y destinatario` |
| HU-03 | Ver detalle e historial | CP-11 a CP-16 | `feat(detalle): agregar vista de detalle con historial de estados` |
| HU-04 | Cambiar estado con auditoría | CP-13 a CP-16 | `feat(estados): agregar transición de estado con auditoría` |
| HU-06 | Login con rol | CP-25 a CP-30 | `feat(auth): agregar login con control de acceso por roles` |
| HU-10 | Listado paginado | CP-07 a CP-10 | `feat(listado): agregar paginación de 20 ítems por página` |
| HU-32 | Dataset IA | CP-31, CP-32 | `feat(ia): agregar dataset simulado de 500 registros` |
| HU-33 | Modelo ML predicción | CP-33, CP-34 | `feat(ia): implementar modelo de predicción de demoras` |
| HU-34 | Predicción al registrar | CP-35, CP-36 | `feat(ia): agregar interfaz de predicción en prototipo` |

## Links relevantes

- 📋 [Tablero Trello](https://trello.com) *(reemplazar con link real)*
- 📄 [Documentación del proyecto](./docs/)
- 🔁 [Historial de CI](https://github.com/TU_USUARIO/logitrack/actions)

---

*Universidad Nacional de General Sarmiento — Laboratorio de Construcción de Software — 1C 2026*
