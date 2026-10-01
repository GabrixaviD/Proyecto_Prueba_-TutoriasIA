"""Excepciones de busqueda de peliculas y series."""

from .base import AppError


class MovieNotFoundError(AppError):
    """La pelicula solicitada no existe en la fuente consultada."""

    def __init__(self, title: str) -> None:
        super().__init__(f"Pelicula no encontrada: {title}", code="MOV-4041")
        self.title = title


class SeriesNotFoundError(AppError):
    """La serie solicitada no existe en la fuente consultada."""

    def __init__(self, title: str) -> None:
        super().__init__(f"Serie no encontrada: {title}", code="SER-4041")
        self.title = title


__all__ = ["MovieNotFoundError", "SeriesNotFoundError"]
