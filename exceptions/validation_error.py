"""Excepciones de configuracion y validacion de entrada."""

from .base import AppError


class ConfigError(AppError):
    """Configuracion ausente o invalida."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CFG-4001")


class ValidationError(AppError):
    """Entrada de usuario o parametro invalido."""

    def __init__(self, field: str, issue: str) -> None:
        super().__init__(f"Campo '{field}': {issue}", code="VAL-4002")
        self.field = field
        self.issue = issue


__all__ = ["ConfigError", "ValidationError"]
