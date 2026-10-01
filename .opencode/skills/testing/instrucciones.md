# Instrucciones — Skill Testing

Propósito: crear tests automáticos para validar el código.

## Reglas

1. **Estructura de tests/ con pytest.**
   Un archivo por módulo (`tests/test_<modulo>.py`), config central en `pytest.ini`.
   Tests herméticos: sin red, sin archivos fuera de tmp, sin estado residual.

2. **Tests unitarios para servicios.**
   Un test por comportamiento (feliz, no-encontrado, error, caché),
   con nombres descriptivos del escenario.

3. **Mock de APIs externas con pytest-mock.**
   `unittest.mock.patch` (o fixture `mocker`); parchear donde se usa, no donde se define.
   Fake mínimo de respuesta HTTP. Migrar los mocks junto con el código.

4. **Fixtures para datos de prueba.**
   `conftest.py`: variables de entorno, `isolated_fs` (tmp), payloads canónicos,
   limpieza de cachés entre tests. Datos en fixtures, no hardcodeados.

5. **Parametrización de tests.**
   `@pytest.mark.parametrize` con `(entrada, esperado)`; un caso por fila.
   Preferir parametrize sobre bucles dentro del test.

6. **Coverage con pytest-cov.**
   Declarar cada módulo en `pytest.ini`, umbral `--cov-fail-under=80`.
   Cada línea `Missing` del reporte es un test pendiente.

7. **Tests de integración.**
   HTTP mockeado + flujo real de servicio (caché, validación, errores tipados).
   Verificar efectos: llamadas a red, params, timeouts, archivos (vía `isolated_fs`).

8. **Arrange-Act-Assert pattern.**
   Tres bloques visibles por test, un concepto por test,
   asserts sobre valores y efectos.

## Verificación

```bash
python -m pytest -q   # todo en verde
python -m pytest      # cobertura >= 80%
```
