# Instrucciones — Skill Refactoring

Propósito: eliminar malas prácticas del código y mejorar su estructura.

## Reglas

1. **Buscar y eliminar variables globales.**
   Mover el estado a módulos de servicio o pasarlo como argumento.
   Si hay código legacy, exponer los mismos objetos desde un shim de compatibilidad.

2. **Reemplazar wildcard imports por imports específicos.**
   Enumerar solo los nombres necesarios y definir `__all__` en cada módulo público.

3. **Convertir concatenación de strings a f-strings.**
   Mantener la salida byte-idéntica (cuidado con el espaciado en líneas partidas).

4. **Agregar type hints a funciones.**
   Todas las funciones públicas con firma completa (`param: tipo`) y tipo de retorno (`->`).

5. **Separar responsabilidades en módulos.**
   Capas: `api/` (HTTP), `services/` (negocio + estado), `ui/` (consola),
   `models/` (datos), `exceptions/` (errores), `main.py` solo como entrada.
   Actualizar los mocks de los tests a las nuevas ubicaciones.

6. **Eliminar código duplicado.**
   Extraer helpers compartidos, consolidar configuración, archivar obsoletos en `legacy/`.

7. **Reemplazar bare except por excepciones específicas.**
   Jerarquía propia (`AppError` + subclases con `code` y `message`), logging del error,
   salida controlada en el entry point.

8. **Crear dataclasses para modelos de datos.**
   Un `@dataclass` por entidad con `from_<origen>()` validado y `to_dict()`.

9. **Implementar inyección de dependencias.**
   Configuración, claves y clientes HTTP entran como parámetros/objetos inyectables;
   en tests, inyectar fakes con mocks o fixtures, nunca red real.

## Verificación

```bash
python -m pytest -q   # todo en verde, cobertura >= 80%
```
