# Instrucciones — Skill API Integration

Propósito: conectar a APIs REST de forma robusta y mantenible.

## Reglas

1. **Crear clientes para cada API.**
   Un módulo por API (`api/omdb.py`, `api/tvmaze.py`).
   Usar `params=` en los requests, nunca concatenar la query a mano.
   Base URL y rutas en `constants.py`.

2. **Implementar caché de respuestas.**
   Caché en memoria en `services/`, claveada por parámetro normalizado.
   Limpiarla entre tests para evitar contaminación cruzada.

3. **Agregar reintentos con backoff exponencial.**
   Solo para errores transitorios (5xx, timeout, conexión).
   `delay = base * 2**intento` con tope; al agotarse, lanzar `ApiError`.

4. **Manejar rate limiting.**
   Respetar 429 con `Retry-After`; 401/403/404 fallan de inmediato con error tipado.

5. **Validar respuestas con dataclasses.**
   La capa `api/` devuelve JSON crudo; `models/<entidad>.py` valida
   (`from_<origen>()` + `to_dict()`). Datos inválidos → `ValidationError`.

6. **Logging de requests y responses.**
   `logging` con URL en `debug` (solo si `CONFIG.debug`), status en `verbose`,
   errores con `code`. Nunca loguear API keys.

7. **Timeouts configurables.**
   Todo request con `timeout=CONFIG.api.timeout`.
   `requests.Timeout` → `ApiTimeoutError`; el resto → `ApiError`.

8. **Manejo de errores HTTP.**
   Jerarquía `AppError` (`ApiError`, `ApiTimeoutError`, `*NotFoundError`, `ConfigError`).
   Chequear `status_code` antes de parsear JSON; envolver `response.json()` en try/except.

## Verificación

```bash
python -m pytest -q tests/test_api_movies.py   # sin red real (mocks)
```
