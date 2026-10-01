"""Excepciones de integracion con APIs externas (OMDB, TVMaze)."""

from .base import AppError


class ApiError(AppError):
    """Fallo de comunicacion o respuesta invalida de una API externa."""

    def __init__(self, message: str, code: str = "API-5001", status: int | None = None) -> None:
        super().__init__(message, code=code)
        self.status = status


class ApiTimeoutError(ApiError):
    """La API externa no respondio dentro del tiempo limite."""

    def __init__(self, service: str, timeout: int) -> None:
        super().__init__(
            f"{service} no respondio en {timeout}s",
            code="API-5008",
        )


__all__ = ["ApiError", "ApiTimeoutError"]
