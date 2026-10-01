---
name: refactoring
description: Use when refactoring Python code with bad practices — global variables, wildcard imports, string concatenation, missing type hints, duplicated code, bare except clauses, god modules, missing separation of responsibilities, or missing dataclasses for data models.
---

# Python Refactoring — Eliminar malas prácticas

Aplica estas 9 reglas en orden. Después de cada cambio, verifica que la suite siga en verde.

## 1. Buscar y eliminar variables globales

- Detecta: `grep -n "^[A-Z_]* = " *.py` y `global ` en funciones.
- Mueve el estado a módulos de servicio (`services/`) o pásalo como argumento. Si hay código legacy que los importa, expón el **mismo objeto** re-exportado desde un shim de compatibilidad.
- Verifica: `pytest -q` en verde y los tests de identidad de objetos (`is`) siguen pasando.

## 2. Reemplazar wildcard imports por imports específicos

- Detecta: `grep -rn "from .* import \*"`.
- Enumera solo los nombres necesarios (`from x import a, b`) y define `__all__` en cada módulo público.
- Verifica: no hay `import *` restante y `pytest -q` verde.

## 3. Convertir concatenación de strings a f-strings

- Detecta: `grep -n '" *+ *\|+ *f"' *.py` (uniones con `+`).
- Convierte a f-strings. Ojo: en líneas partidas, `("..." "...")` no añade espacio — solo cambia `+` por f-string cuando el `+` aporta el separador.
- Verifica con un diff o un test de salida byte-idéntica.

## 4. Agregar type hints a funciones

- Todas las funciones públicas llevan firma completa: `def f(a: str, n: int = 0) -> dict[str, Any]:`.
- Usa `Any` solo para payloads JSON; evita `Optional` implícitos (parámetros `None` solo con valor por defecto).
- Verifica: cuenta `def` sin `->` y deja el marcador en 0.

## 5. Separar responsabilidades en módulos

- Regla: `api/` (HTTP), `services/` (negocio + estado), `ui/` (consola), `models/` (datos), `exceptions/` (errores), `main.py` solo como punto de entrada.
- Mueve código por capas; deja un **shim delgado** en el módulo original para no romper importadores (`api_movies.py` re-exporta desde `services/`, `api/`, `models/`).
- Actualiza los tests: los mocks deben parchear la **nueva ubicación** (ej. `api.omdb.requests.get`, no `api_movies.requests.get`).

## 6. Eliminar código duplicado

- Detecta: busca funciones con cuerpos casi idénticos (`mostrar_pelicula`/`mostrar_serie`, detectores duplicados) y archivos `*_config.py` redundantes.
- Extrae helpers compartidos (ej. `print_header`, `mostrar_detalle`) y consolida configuración en un solo `config.py` + `constants.py`.
- Archiva lo obsoleto en `legacy/` en vez de borrarlo si hay riesgo de referencias.

## 7. Reemplazar bare except por excepciones específicas

- Detecta: `grep -rn "except:"`.
- Crea una jerarquía en `exceptions/` (`AppError` base con `code` + `message`; subclases: `MovieNotFoundError`, `ApiError`, `ApiTimeoutError`, `ConfigError`, `ValidationError`).
- Regla: `except (OSError, ValueError) as exc:` + `logger.error(...)`; en el entry point, `except AppError` → `sys.exit(1)`.

## 8. Crear dataclasses para modelos de datos

- Un `@dataclass(frozen=True)` por entidad en `models/`, con `from_<origen>()` (ej. `from_omdb`, `from_tvmaze`) que valide campos requeridos y lance `ValidationError`, más `to_dict()` para serializar.
- La capa `services/` traduce dicts crudos → modelos; la capa `api/` devuelve JSON crudo.

## 9. Implementar inyección de dependencias

- Ninguna función de negocio construye su propia dependencia: la configuración entra por `CONFIG` (objeto inyectable, testeable), la key por parámetro/entorno (`require_api_key()`), el HTTP por `requests` mockeable.
- En tests, inyecta fakes con `unittest.mock.patch` o fixtures; nunca red real.

## Verificación final

```bash
python -m pytest -q        # todo en verde
python -m pytest -q        # cobertura >= 80% (umbral en pytest.ini)
```

Ejemplo (este repo): 118 passed, cobertura 100%.
