"""Servicio de series: busqueda y detalle con cache (Fase 3)."""

from typing import Any

from api.tvmaze import search_shows as _api_search_shows
from api.tvmaze import show_details as _api_show_details
from utils import validate_positive_int, validate_search_query

# Estado del servicio (antes: globales de api_movies.py)
CACHE_SERIES: dict[str, Any] = {}


def buscar_series(nombre: str) -> list[dict[str, Any]]:
    """Busca series en TVMaze con validacion y cache."""

    nombre = validate_search_query(nombre, "nombre")
    cache_key = f"series_{nombre}"
    if cache_key in CACHE_SERIES:
        return CACHE_SERIES[cache_key]

    data = _api_search_shows(nombre)

    CACHE_SERIES[cache_key] = data
    return data


def obtener_detalles_serie(id_serie: int) -> dict[str, Any]:
    """Obtiene detalles de serie con id validado."""

    serie_id = validate_positive_int(id_serie, "id_serie")
    return _api_show_details(serie_id)


__all__ = ["CACHE_SERIES", "buscar_series", "obtener_detalles_serie"]
