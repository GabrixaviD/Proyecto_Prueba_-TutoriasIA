"""Cliente HTTP de OMDB + request compartido con manejo tipado (Fase 3/4)."""

import logging
from typing import Any

import requests

from config import CONFIG
from constants import OMDB_SEARCH_BY_ACTOR_PATH, OMDB_SEARCH_BY_TITLE_PATH
from exceptions import ApiError, ApiTimeoutError

logger = logging.getLogger("movies.api")


def hacer_request(url: str, params: dict[str, Any] | None = None) -> Any:
    """Hace request con manejo de errores tipado (timeout, HTTP, JSON)."""

    if CONFIG.debug:
        logger.debug("Haciendo request a %s", url)

    try:
        response = requests.get(url, params=params, timeout=CONFIG.api.timeout)
    except requests.Timeout as exc:
        raise ApiTimeoutError(url, CONFIG.api.timeout) from exc
    except requests.RequestException as exc:
        raise ApiError(f"Error de red contra {url}: {exc}") from exc

    if CONFIG.verbose:
        logger.debug("Status code: %s", response.status_code)

    if response.status_code != 200:
        raise ApiError(
            f"API respondio con estado {response.status_code}",
            status=response.status_code,
        )

    try:
        return response.json()
    except ValueError as exc:
        raise ApiError(f"Respuesta no es JSON valido: {exc}") from exc


def search_by_title(titulo: str, api_key: str) -> dict[str, Any]:
    """Busca una pelicula por titulo en OMDB (respuesta cruda)."""

    url = f"{CONFIG.api.omdb_url}{OMDB_SEARCH_BY_TITLE_PATH}"
    return hacer_request(url, params={"t": titulo, "apikey": api_key})


def search_by_actor(actor: str, api_key: str) -> dict[str, Any]:
    """Busca peliculas por actor en OMDB (respuesta cruda)."""

    url = f"{CONFIG.api.omdb_url}{OMDB_SEARCH_BY_ACTOR_PATH}"
    return hacer_request(
        url, params={"s": actor, "type": "movie", "apikey": api_key}
    )


__all__ = ["hacer_request", "search_by_actor", "search_by_title"]
