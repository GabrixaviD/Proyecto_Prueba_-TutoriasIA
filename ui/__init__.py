"""Capa de interfaz de consola: display y menu."""

from .display import (
    clear_screen,
    mostrar_lista_peliculas,
    mostrar_pelicula,
    mostrar_serie,
    print_header,
    print_separator,
)
from .menu import menu_principal

__all__ = [
    "clear_screen",
    "menu_principal",
    "mostrar_lista_peliculas",
    "mostrar_pelicula",
    "mostrar_serie",
    "print_header",
    "print_separator",
]
