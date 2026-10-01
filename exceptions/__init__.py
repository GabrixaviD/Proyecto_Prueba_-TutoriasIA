"""Paquete de excepciones personalizadas de la aplicacion."""

from .api_error import ApiError, ApiTimeoutError
from .base import AppError
from .movie_not_found import MovieNotFoundError, SeriesNotFoundError
from .validation_error import ConfigError, ValidationError

__all__ = [
    "ApiError",
    "ApiTimeoutError",
    "AppError",
    "ConfigError",
    "MovieNotFoundError",
    "SeriesNotFoundError",
    "ValidationError",
]
