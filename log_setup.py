"""Configuracion central del modulo logging.

Unifica los loggers caseros (``logger.py``, ``log_manager.py``) bajo el
``logging`` estandar: archivo rotativo + consola.
"""

import logging
from logging.handlers import RotatingFileHandler

_configured = False


def setup_logging(level: str = "INFO", log_file: str = "app.log") -> logging.Logger:
    """Configura el logger raiz una sola vez y lo devuelve."""

    global _configured
    logger = logging.getLogger("movies")
    if _configured:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    _configured = True
    return logger


def get_logger(name: str = "movies") -> logging.Logger:
    """Devuelve un logger hijo ya configurado."""

    setup_logging()
    return logging.getLogger(name)
