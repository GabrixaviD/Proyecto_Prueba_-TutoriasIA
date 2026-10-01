"""Compatibilidad: re-exporta la API publica desde api/ y services/ (Fase 3).

El codigo nuevo debe importar desde ``api``, ``services`` o ``models``.
Este modulo se conserva para no romper importadores existentes.
"""

from api.omdb import hacer_request
from services.movie_service import (
    CACHE_PELICULAS,
    HISTORIAL_BUSQUEDAS,
    PELICULAS_FAVORITAS,
    USUARIO_LOGUEADO,
    agregar_a_favoritas,
    agregar_al_historial,
    buscar_pelicula,
    buscar_peliculas_por_actor,
    buscar_peliculas_por_genero,
    eliminar_de_favoritas,
    exportar_a_json,
    importar_de_json,
    limpiar_historial,
    obtener_estadisticas,
    obtener_peliculas_populares,
)
from services.series_service import (
    CACHE_SERIES,
    buscar_series,
    obtener_detalles_serie,
)

__all__ = [
    "CACHE_PELICULAS",
    "CACHE_SERIES",
    "HISTORIAL_BUSQUEDAS",
    "PELICULAS_FAVORITAS",
    "USUARIO_LOGUEADO",
    "agregar_a_favoritas",
    "agregar_al_historial",
    "buscar_pelicula",
    "buscar_peliculas_por_actor",
    "buscar_peliculas_por_genero",
    "buscar_series",
    "eliminar_de_favoritas",
    "exportar_a_json",
    "hacer_request",
    "importar_de_json",
    "limpiar_historial",
    "obtener_detalles_serie",
    "obtener_estadisticas",
    "obtener_peliculas_populares",
]
