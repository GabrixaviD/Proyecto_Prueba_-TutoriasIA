---
name: api-integration
description: Use when integrating REST APIs in Python — per-API HTTP clients, response caching, retries with exponential backoff, rate limiting, response validation with dataclasses, request/response logging, configurable timeouts, or typed HTTP error handling.
---

# API Integration — Conectar a APIs REST robustamente

Un cliente por API externa, con la misma estructura. Referencia: `api/omdb.py`, `api/tvmaze.py` + `exceptions/api_error.py`.

## 1. Crear clientes para cada API

- Un módulo por API (`api/omdb.py`, `api/tvmaze.py`) con funciones de dominio (`search_by_title`, `show_details`) que devuelven JSON crudo.
- Un único `hacer_request(url, params)` compartido: usa `params=` (nunca concatenes la query a mano — el encoding lo hace `requests`).
- Base URL y rutas en `constants.py` (`OMDB_SEARCH_BY_TITLE_PATH`, ...); nada hardcodeado en el cliente.

## 2. Implementar caché de respuestas

- Caché en memoria en la capa `services/` (`CACHE_PELICULAS`, `CACHE_SERIES: dict`), claveada por parámetro normalizado (título en minúsculas, URL completa).
- Flujo: mirar caché → si falta, llamar a `api/` → guardar → devolver.
- En tests, limpia la caché entre casos (`conftest.py`: `autouse` fixture con `.clear()`) para evitar contaminación cruzada.

## 3. Agregar reintentos con backoff exponencial

- Reintenta solo errores transitorios (5xx, timeout, conexión); nunca 4xx ni errores de validación.
- Backoff: `delay = base * 2**intento` con tope máximo y un máximo de intentos configurable.
- Si se agotan los intentos, lanza `ApiError` con la causa encadenada (`from exc`).

## 4. Manejar rate limiting

- Respeta el código 429: lee el header `Retry-After` y espera ese tiempo antes de reintentar.
- Serializa llamadas si la API lo exige; documenta el límite en el docstring del cliente.
- Distingue 429 (esperar + reintentar) de 401/403/404 (fallar de inmediato con error tipado).

## 5. Validar respuestas con dataclasses

- La capa `api/` devuelve JSON crudo; la **validación** vive en `models/<entidad>.py` (`Movie.from_omdb`, `Series.from_tvmaze`).
- `from_<origen>()` verifica campos requeridos y tipos; ante datos inválidos lanza `ValidationError` con `code` (ej. `VAL-5001`). Regla: jamás valides con `assert` en producción.
- Añade `to_dict()` para serializar el modelo de vuelta.

## 6. Logging de requests y responses

- `logger = logging.getLogger("movies.api")`; loguea la URL en `debug` solo si `CONFIG.debug` está activo (evita ruido y filtrado de keys en prod).
- Loguea el `status_code` en modo `verbose`; errores con `logger.error("[%s] %s", code, message)`.
- Nunca imprimas API keys en logs; la key viaja solo en `params`.

## 7. Timeouts configurables

- Todo request lleva `timeout=CONFIG.api.timeout` (valor central en `config.py`, sobreescribible por entorno).
- Distingue `requests.Timeout` → `ApiTimeoutError(url, timeout)` de otros `requests.RequestException` → `ApiError`.
- En la UI, el timeout se captura como `AppError` y el menú sobrevive (no `sys.exit` desde funciones de menú).

## 8. Manejo de errores HTTP

- Jerarquía en `exceptions/`: `AppError(code, message)` base; `ApiError(status?)`, `ApiTimeoutError`, más `MovieNotFoundError`/`SeriesNotFoundError` para "no encontrado" de negocio (ej. `Response == "False"` en OMDB).
- Chequea `response.status_code != 200` antes de parsear JSON; envuelve `response.json()` en `try/except ValueError` → `ApiError("Respuesta no es JSON valido")`.
- Las claves/API faltantes son `ConfigError` (`require_api_key()`), no `ApiError`.

## Verificación

```bash
python -m pytest -q tests/test_api_movies.py   # mocks sobre api.omdb.requests.get, sin red real
```
