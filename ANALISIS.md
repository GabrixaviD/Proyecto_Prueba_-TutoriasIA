# FASE 1 — Análisis del código

Proyecto: Películas y Series · Fecha: 2026-10-01 · ~120 archivos `.py` en raíz (estructura plana).

## 1. Variables globales en `api_movies.py` y `main.py`

| Módulo | Globales | Estado tras Fases 4-6 |
|---|---|---|
| `api_movies.py` | `USUARIO_LOGUEADO`, `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_PELICULAS`, `CACHE_SERIES` | ⏳ Pendientes (objetivo Fase 3: encapsular en `services/`) |
| `main.py` | _(ninguna)_ | ✅ Sin `global` |
| `app.py` (legado) | `API_KEY`, `OMDB_BASE_URL`, `TVMAZE_BASE_URL`, `CACHE`, `USUARIO_ACTUAL`, `PELICULAS_FAVORITAS`, `HISTORIAL` | ⏳ Duplicado de `main.py`; consolidar o eliminar |

Además, cada `*_manager.py` mantiene estado global propio (`users`, `favorites`, …) + persistencia JSON.

## 2. Mapa de dependencias entre módulos

Acoplamiento real (imports locales):

- `main.py` → `api_movies`, `config`, `constants`, `log_setup`
- `api_movies.py` → `config`, `constants`, `utils`
- `app.py` → `log_setup`
- `config.py` → `exceptions`
- `utils.py` → `exceptions`
- `tests/*` → todos los módulos refactorizados

Hallazgo: los ~25 `*_manager.py` **no se importan entre sí ni desde `main.py`** — son
islas autónomas con estado global propio (bajo acoplamiento, alta duplicación interna:
todos repiten `load_/save_/export_/import_/backup_/restore_/validate_`).

## 3. Duplicación de código identificada

| Caso | Alcance | Acción propuesta |
|---|---|---|
| `app.py` ≈ `main.py` (13 funciones: `menu_principal`, `mostrar_pelicula`, `funcion_buscar_*`, …) | ~250 líneas | Eliminar `app.py` o dejarlo como alias; `main.py` es el entry point (`python main.py`) |
| `logger.py` vs `log_manager.py` vs `log_config.py` | 3 loggers caseros | ✅ Reemplazados por `log_setup.py` (Fase 4); archivar los 3 |
| `config_manager.py` vs `config_manager_v2.py` vs `config.py` | 3 configs | ✅ `config.py` es canónico (Fase 5); archivar los otros 2 |
| `cache_manager.py` vs `cache_manager_v2.py` | 2 caches | Archivar/duplicado por resolver |
| Patrón `load/save/export/import/backup/restore/validate` en cada manager | ~25 archivos | Objetivo Fase 3: clase base `services/base_service.py` |
| `format_movie_display` (`utils.py`) ≈ `mostrar_pelicula` (`main.py`) | 2 formateadores | Unificar en `ui/display.py` (Fase 3) |

## 4. Bare `except` y manejo de errores deficiente

✅ **Resuelto en Fase 4** (verificación: 0 `except:` en el proyecto):

- 17 `bare except` → excepciones específicas (`.get()` en accesos a dict,
  `(OSError, ValueError)` en IO, `(TypeError, KeyError, AttributeError)` en ordenamientos).
- 2 `except Exception` top-level (`app.py`, `main.py`) → `except AppError` + `logger.exception`.
- `hacer_request` lanza `ApiError`/`ApiTimeoutError` tipados en vez de fallar en silencio.
- Logging central `log_setup.py` (`RotatingFileHandler` 10 MB × 3 + consola WARNING+).

## 5. Archivos `*_config.py` que no se usan

- **Total: 88 archivos** (`api_cache_*_config.py` × ~50 + `api_*_config.py` + `theme/language/ui/…`).
- **Importados por código de aplicación: 0** (verificado por grep en `main.py`, `app.py`,
  `api_movies.py`, `config.py`, `constants.py`).
- Reemplazo canónico: `config.py` (dataclasses + env vars, 100% tests).
- Acción propuesta (Fase 2): mover los 88 a `legacy/config_bak/` (no borrar: referencia
  histórica) y dejar `config.py` como única fuente.
