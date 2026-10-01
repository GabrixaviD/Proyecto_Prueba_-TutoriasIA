---
name: testing
description: Use when creating automated tests with pytest — tests/ layout, unit tests for services, mocking external APIs, fixtures for test data, test parametrization, coverage with pytest-cov, integration tests, or the Arrange-Act-Assert pattern.
---

# Testing — Crear tests automáticos con pytest

Referencia: `tests/`, `tests/conftest.py`, `pytest.ini`. Ejemplo (este repo): 118 passed, cobertura 100%.

## 1. Estructura de tests/ con pytest

- Un archivo por módulo testeado: `tests/test_<modulo>.py` (`test_api_movies.py`, `test_models.py`, ...).
- `pytest.ini` centraliza la config: `testpaths = tests`, `addopts` con `--cov=<modulo>` por cada módulo cubierto + `--cov-report=term-missing` + `--cov-fail-under=80`.
- Ejecución estándar: `python -m pytest -q` (rápida, sin cobertura) y `python -m pytest` (con cobertura según `pytest.ini`).
- Todo test debe ser hermético: sin red, sin archivos fuera de tmp, sin estado global residual.

## 2. Tests unitarios para servicios

- Un test por comportamiento: caso feliz, caso "no encontrado", caso error, caso caché.
- Nombres descriptivos en español con el escenario: `test_buscar_pelicula_ok_y_cache`, `test_buscar_pelicula_no_encontrada`.
- La función bajo test se importa desde su ubicación real (`services`, `api`, `models`); el shim de compatibilidad (`api_movies`) se testea solo por re-exportación.

## 3. Mock de APIs externas

- Usa `unittest.mock.patch` (estándar; `pytest-mock` es equivalente con fixture `mocker`).
- Parchea **donde se usa**, no donde se define: `api.omdb.requests.get` (nueva ubicación tras Fase 3), `services.series_service._api_show_details`.
- Fake mínimo de respuesta HTTP:
  ```python
  class FakeResponse:
      def __init__(self, data, status=200, bad_json=False): ...
      def json(self): ...
  ```
- Tras migrar código de módulo, migra los mocks con él (`api_movies.requests` → `api.omdb.requests`) — un `AttributeError: module has no attribute 'requests'` indica mock obsoleto.

## 4. Fixtures para datos de prueba

- `tests/conftest.py` con fixtures compartidas:
  - `OMDB_API_KEY=test-key` fijada en entorno al importar (los servicios exigen key incluso mockeados).
  - `isolated_fs`: `chdir` a `tmp_path` para tests que escriben archivos (export/import).
  - `sample_movie`: payload canónico reutilizado.
  - Fixture `autouse` que limpia cachés (`CACHE_PELICULAS.clear()`, etc.) entre tests.
- Regla: datos de prueba en fixtures, nunca hardcodeados en cada test.

## 5. Parametrización de tests

- Usa `@pytest.mark.parametrize` para el mismo comportamiento con varias entradas (ej. géneros válidos/inválidos, códigos de error HTTP).
- Un caso por fila: `(entrada, esperado)`; el nombre del test describe la dimensión variada.
- Prefiere parametrize sobre bucles `for` dentro del test (cada caso falla/Worksheet por separado).

## 6. Coverage con pytest-cov

- Declara cada módulo en `pytest.ini` (`--cov=api`, `--cov=services`, `--cov=models`, ...); lo no medido no mejora.
- Umbral de fallo: `--cov-fail-under=80` (este repo exige el equivalente al 100% real: 118 tests / 100%).
- Lee el reporte `term-missing`: cada línea `Missing` es un test pendiente — añade el test que la cubre (ej. `test_show_details_url_usa_id_validado` cubrió `api/tvmaze.py:20-21`).
- La UI interactiva (`ui/menu.py`) se excluye de cobertura: se verifica con ejecución manual, no con tests.

## 7. Tests de integración

- Archivos `test_api_movies.py`: HTTP mockeado (FakeResponse), flujo real de servicio (caché, historial, validación, errores tipados) — sin red real.
- Verifica efectos colaterales: segunda llamada no pega a red (`mock_get.call_count == 1`), `kwargs["params"]` lleva el encoding, `kwargs["timeout"] == CONFIG.api.timeout`.
- Integración con archivos reales vía `isolated_fs` (export/import JSON round-trip).

## 8. Arrange-Act-Assert pattern

- Estructura cada test en tres bloques visibles:
  ```python
  def test_agregar_a_favoritas_duplicado():
      pelicula = {"Title": "Matrix"}          # Arrange
      agregar_a_favoritas(pelicula)            # Act
      assert agregar_a_favoritas(pelicula) is False  # Assert
      assert len(PELICULAS_FAVORITAS) == 1     # Assert (efecto)
  ```
- Un concepto por test; si necesitas "y" en el nombre, probablemente son dos tests.
- Asserts sobre valores y sobre efectos (estado, llamadas a mocks, archivos), no solo sobre "no lanzó excepción".

## Verificación final

```bash
python -m pytest -q          # N passed, 0 failed
python -m pytest             # cobertura >= 80%, sin líneas Missing inesperadas
```
