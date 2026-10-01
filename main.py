"""Punto de entrada: `python main.py` (Fase 3).

Toda la logica vive en `ui/`, `services/`, `api/` y `models/`.
"""

import logging
import sys

from exceptions import AppError
from log_setup import setup_logging
from ui.menu import menu_principal

setup_logging()
logger = logging.getLogger("movies.main")


# Programa principal
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except AppError as e:
        logger.critical("[%s] %s", e.code, e.message)
        print(f"Error [{e.code}]: {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Error inesperado: %s", e)
        print(f"Error inesperado: {e}")
        sys.exit(1)
