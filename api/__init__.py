"""Capa de acceso a APIs externas: OMDB y TVMaze."""

from .omdb import hacer_request, search_by_actor, search_by_title
from .tvmaze import search_shows, show_details

__all__ = [
    "hacer_request",
    "search_by_actor",
    "search_by_title",
    "search_shows",
    "show_details",
]
