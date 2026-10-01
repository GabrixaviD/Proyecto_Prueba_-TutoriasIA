"""Cliente HTTP de TVMaze (Fase 3)."""

from typing import Any

from api.omdb import hacer_request
from config import CONFIG
from constants import TVMAZE_SEARCH_SHOWS_PATH, TVMAZE_SHOW_DETAILS_PATH


def search_shows(nombre: str) -> Any:
    """Busca series por nombre en TVMaze (respuesta cruda)."""

    url = f"{CONFIG.api.tvmaze_url}{TVMAZE_SEARCH_SHOWS_PATH}"
    return hacer_request(url, params={"q": nombre})


def show_details(serie_id: int) -> dict[str, Any]:
    """Obtiene el detalle de una serie por id (respuesta cruda)."""

    url = f"{CONFIG.api.tvmaze_url}{TVMAZE_SHOW_DETAILS_PATH}{serie_id}"
    return hacer_request(url)


__all__ = ["search_shows", "show_details"]
