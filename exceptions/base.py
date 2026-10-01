"""Excepciones base de la aplicacion Peliculas y Series."""


class AppError(Exception):
    """Error base con codigo estable para el envelope de errores."""

    def __init__(self, message: str, code: str = "APP-0000") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


__all__ = ["AppError"]
