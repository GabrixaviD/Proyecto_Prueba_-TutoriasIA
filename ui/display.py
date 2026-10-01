"""Visualizacion por consola: separadores, fichas y listas (Fase 3)."""

import os
from typing import Any

from constants import DISPLAY_WIDTH, SEPARATOR_CHARACTER


def clear_screen() -> None:
    """Limpia pantalla de forma no portable."""
    os.system("cls" if os.name == "nt" else "clear")


def print_separator() -> None:
    """Imprime separador."""
    print(SEPARATOR_CHARACTER * DISPLAY_WIDTH)


def print_header(text: str) -> None:
    """Imprime header."""
    print_separator()
    print(text.upper().center(DISPLAY_WIDTH))
    print_separator()


def mostrar_pelicula(pelicula: dict[str, Any] | None) -> None:
    """Muestra pelicula con acceso seguro a claves (ausentes -> N/A)."""
    print_separator()
    if pelicula is None:
        print("No se encontró la película")
        return

    # Acceso seguro con .get(): claves ausentes -> "N/A" sin excepciones
    fields = [
        ("Título", "Title"),
        ("Año", "Year"),
        ("Rating IMDB", "imdbRating"),
        ("Género", "Genre"),
        ("Director", "Director"),
        ("Actores", "Actors"),
        ("Trama", "Plot"),
        ("País", "Country"),
        ("Premios", "Awards"),
    ]
    for label, key in fields:
        print(f"{label}: {pelicula.get(key, 'N/A')}")

    print_separator()


def mostrar_serie(serie: dict[str, Any]) -> None:
    """Muestra serie."""
    print_separator()
    show = serie.get("show", serie)

    print(f"Nombre: {show.get('name', 'N/A')}")
    print(f"Idioma: {show.get('language', 'N/A')}")
    print(f"Géneros: {show.get('genres', [])}")
    print(f"Rating: {show.get('rating', {}).get('average', 'N/A')}")
    print(f"Estado: {show.get('status', 'N/A')}")
    print(f"Estreno: {show.get('premiered', 'N/A')}")
    print(f"Final: {show.get('ended', 'N/A')}")
    print(f"Episodios: {show.get('runtime', 'N/A')}")
    summary = str(show.get("summary", "N/A"))
    if len(summary) > 200:
        summary = f"{summary[:200]}..."
    print(f"Resumen: {summary}")
    print_separator()


def mostrar_lista_peliculas(peliculas: list[dict[str, Any]]) -> None:
    """Muestra lista de peliculas."""
    i = 0
    while i < len(peliculas):
        if "titulo" in peliculas[i]:
            print(
                f"{i + 1}. {peliculas[i]['titulo']} "
                f"({peliculas[i]['anio']}) - {peliculas[i]['rating']}"
            )
        elif "Title" in peliculas[i]:
            print(
                f"{i + 1}. {peliculas[i]['Title']} "
                f"({peliculas[i].get('Year', 'N/A')})"
            )
        else:
            print(f"{i + 1}. Película desconocida")
        i += 1


__all__ = [
    "clear_screen",
    "mostrar_lista_peliculas",
    "mostrar_pelicula",
    "mostrar_serie",
    "print_header",
    "print_separator",
]
