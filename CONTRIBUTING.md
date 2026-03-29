# Guía de Contribución — LogiTrack

Este documento define los estándares de trabajo del equipo para el proyecto LogiTrack.

---

## Estrategia de Ramas (GitHub Flow)

Adoptamos **GitHub Flow**: una rama `main` estable y ramas de funcionalidad por historia de usuario.

### Ramas disponibles

| Rama | Propósito | Reglas |
|------|-----------|--------|
| `main` | Rama estable de producción | Solo recibe merges vía PR aprobado. Siempre debe estar verde en CI. |
| `feature/HU-XX` | Desarrollo de una HU específica | Se crea desde `main`. Nombre: `feature/` + ID de HU (ej: `feature/HU-01`). |
| `fix/descripcion` | Corrección de errores | Se crea desde `main`. Nombre: `fix/` + descripción breve. |
| `docs/descripcion` | Cambios en documentación | Se crea desde `main`. Nombre: `docs/` + descripción breve. |

### Flujo de trabajo

```
1. Crear rama desde main:
   git checkout main && git pull
   git checkout -b feature/HU-XX

2. Desarrollar y commitear siguiendo la convención de commits.

3. Hacer push de la rama:
   git push origin feature/HU-XX

4. Abrir Pull Request hacia main en GitHub.

5. Esperar aprobación (mínimo 1 reviewer) y que el CI esté verde.

6. Hacer merge (squash merge recomendado).

7. Eliminar la rama remota luego del merge.
```

---

## Convención de Commits (Conventional Commits)

Los mensajes de commit siguen el estándar [Conventional Commits](https://www.conventionalcommits.org/).

**Formato:**
```
tipo(alcance): descripción breve en español
```

### Tipos permitidos

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feat` | Nueva funcionalidad | `feat(envios): agregar carga masiva de datos de prueba` |
| `fix` | Corrección de error | `fix(busqueda): corregir estado vacío sin resultados` |
| `docs` | Documentación | `docs: agregar documento de entrega semana 3` |
| `test` | Pruebas | `test(envios): agregar test de unicidad de tracking ID` |
| `ci` | Pipeline CI | `ci: agregar workflow de GitHub Actions` |
| `refactor` | Refactorización | `refactor(listado): extraer lógica de paginación` |
| `chore` | Mantenimiento | `chore: actualizar dependencias de package.json` |

### Reglas

- La descripción va en **español**, en minúsculas, sin punto final.
- El `alcance` (scope) es opcional pero recomendado: indica el módulo afectado.
- Para cambios que rompen compatibilidad, agregar `!` después del tipo: `feat!: ...`

---

## Proceso de Code Review

Todo merge a `main` requiere cumplir los siguientes requisitos:

1. **Mínimo 1 aprobación** de otro integrante del equipo.
2. El reviewer debe responder **en menos de 24 horas**.
3. El Pull Request debe incluir:
   - Descripción del cambio realizado.
   - Referencia a la HU asociada (ej: `Cierra #HU-01`).
   - Evidencia de que los tests pasan (el CI debe estar verde).

### Template de Pull Request

Al abrir un PR en GitHub, usar esta estructura:

```
## ¿Qué hace este PR?
Descripción breve del cambio.

## Historia de Usuario relacionada
HU-XX — [Nombre de la HU]

## Checklist
- [ ] Los tests pasan localmente (`npm test`)
- [ ] El linter no reporta errores (`npm run lint`)
- [ ] La documentación fue actualizada si corresponde
- [ ] El CI está verde en esta rama
```

---

## Configuración del entorno de desarrollo

### Requisitos
- Node.js v20 LTS
- Python 3.10+ (para el modelo IA)
- Git 2.x

### Setup inicial
```bash
git clone https://github.com/TU_USUARIO/logitrack.git
cd logitrack
npm install
```

### Scripts disponibles
```bash
npm test        # Ejecutar tests
npm run lint    # Verificación de estilo
```

---

## Estándares de código

- **Indentación:** 2 espacios (JavaScript), 4 espacios (Python).
- **Comillas:** simples en JavaScript.
- **Punto y coma:** obligatorio en JavaScript.
- **Nombres de variables:** camelCase en JS, snake_case en Python.
- **Comentarios:** en español para este proyecto académico.

---

*LogiTrack — UNGS — Laboratorio de Construcción de Software — 1C 2026*
