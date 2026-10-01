"""Servicio de peliculas: busqueda, favoritas, historial y estadisticas (Fase 3)."""

import json
import logging
from typing import Any

from api.omdb import search_by_actor as _api_search_by_actor
from api.omdb import search_by_title as _api_search_by_title
from config import CONFIG, require_api_key
from constants import API_SUCCESS_RESPONSE, MOVIES_BY_GENRE, POPULAR_MOVIES
from utils import validate_search_query

logger = logging.getLogger("movies.services.movies")

# Estado del servicio (antes: globales de api_movies.py)
USUARIO_LOGUEADO: Any = None
PELICULAS_FAVORITAS: list[dict[str, Any]] = []
HISTORIAL_BUSQUEDAS: list[dict[str, Any]] = []
CACHE_PELICULAS: dict[str, Any] = {}


def buscar_pelicula(titulo: str) -> dict[str, Any] | None:
    """Busca pelicula con validacion, cache y API key obligatoria."""

    titulo = validate_search_query(titulo, "titulo")

    if titulo in CACHE_PELICULAS:
        if CONFIG.debug:
            logger.debug("Usando cache para %s", titulo)
        return CACHE_PELICULAS[titulo]

    api_key = require_api_key()  # Falla claro sin OMDB_API_KEY
    data = _api_search_by_title(titulo, api_key)

    if data.get("Response") == API_SUCCESS_RESPONSE:
        CACHE_PELICULAS[titulo] = data
        return data
    return None


def buscar_peliculas_por_actor(actor: str) -> list[dict[str, Any]]:
    """Busca peliculas por actor con validacion de entrada."""

    actor = validate_search_query(actor, "actor")
    api_key = require_api_key()
    data = _api_search_by_actor(actor, api_key)

    if data.get("Response") == API_SUCCESS_RESPONSE:
        return data.get("Search", [])
    return []


def obtener_peliculas_populares() -> list[dict[str, Any]]:
    """Retorna lista de peliculas populares (copias, sin mutar el original)."""

    return [movie.copy() for movie in POPULAR_MOVIES]


def buscar_peliculas_por_genero(genero: str) -> list[dict[str, Any]]:
    """Busca por genero en el catalogo local (copias, sin mutar el original)."""

    peliculas = MOVIES_BY_GENRE.get(genero.lower())
    if peliculas is None:
        peliculas = tuple(
            movie for movies in MOVIES_BY_GENRE.values() for movie in movies
        )
    return [movie.copy() for movie in peliculas]


def agregar_a_favoritas(pelicula: dict[str, Any]) -> bool:
    """Agrega a favoritas evitando duplicados por titulo."""

    for existente in PELICULAS_FAVORITAS:
        if existente.get("Title") == pelicula.get("Title"):
            return False
    PELICULAS_FAVORITAS.append(pelicula)
    return True


def eliminar_de_favoritas(titulo: str) -> bool:
    """Elimina de favoritas por titulo; False si no existe."""

    for i, favorita in enumerate(PELICULAS_FAVORITAS):
        if favorita.get("Title") == titulo:
            PELICULAS_FAVORITAS.pop(i)
            return True
    return False


def agregar_al_historial(pelicula: dict[str, Any]) -> None:
    """Agrega una entrada al historial de busquedas."""

    HISTORIAL_BUSQUEDAS.append(
        {"titulo": pelicula.get("Title", ""), "fecha": "hoy"}
    )


def limpiar_historial() -> None:
    """Limpia el historial in-place (preserva la identidad del objeto)."""

    HISTORIAL_BUSQUEDAS.clear()


def obtener_estadisticas() -> dict[str, int]:
    """Cuenta favoritas e historial."""

    return {
        "total_favoritas": len(PELICULAS_FAVORITAS),
        "total_historial": len(HISTORIAL_BUSQUEDAS),
    }


def exportar_a_json(nombre_archivo: str) -> None:
    """Exporta favoritas, historial y estadisticas a JSON."""

    data = {
        "favoritas": PELICULAS_FAVORITAS,
        "historial": HISTORIAL_BUSQUEDAS,
        "estadisticas": obtener_estadisticas(),
    }

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        json.dump(data, file)

    print(f"Exportado a {nombre_archivo}")


def importar_de_json(nombre_archivo: str) -> None:
    """Importa datos in-place (preserva la identidad de los objetos)."""

    with open(nombre_archivo, encoding="utf-8") as file:
        data = json.load(file)

    PELICULAS_FAVORITAS.clear()
    PELICULAS_FAVORITAS.extend(data.get("favoritas", []))
    HISTORIAL_BUSQUEDAS.clear()
    HISTORIAL_BUSQUEDAS.extend(data.get("historial", []))

    print(f"Importado desde {nombre_archivo}")


__all__ = [
    "CACHE_PELICULAS",
    "HISTORIAL_BUSQUEDAS",
    "PELICULAS_FAVORITAS",
    "USUARIO_LOGUEADO",
    "agregar_a_favoritas",
    "agregar_al_historial",
    "buscar_pelicula",
    "buscar_peliculas_por_actor",
    "buscar_peliculas_por_genero",
    "eliminar_de_favoritas",
    "exportar_a_json",
    "importar_de_json",
    "limpiar_historial",
    "obtener_estadisticas",
    "obtener_peliculas_populares",
]
