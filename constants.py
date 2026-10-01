"""Constantes inmutables usadas por la aplicacion."""


# API
OMDB_SEARCH_BY_TITLE_PATH = "?t="
OMDB_SEARCH_BY_ACTOR_PATH = "?s="
OMDB_MOVIE_TYPE_QUERY = "&type=movie"
API_KEY_QUERY = "&apikey="
TVMAZE_SEARCH_SHOWS_PATH = "/search/shows?q="
TVMAZE_SHOW_DETAILS_PATH = "/shows/"
API_SUCCESS_RESPONSE = "True"

# Interfaz de consola
DISPLAY_WIDTH = 60
SEPARATOR_CHARACTER = "="
DEFAULT_DELAY_SECONDS = 1
JSON_EXTENSION = ".json"
MENU_EXIT_OPTION = "12"

# Datos de ejemplo usados por las opciones populares y genero.
POPULAR_MOVIES = (
    {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
    {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
    {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
    {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
    {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8},
)

MOVIES_BY_GENRE = {
    "accion": (
        {"titulo": "Die Hard", "anio": 1988, "rating": 8.2},
        {"titulo": "Mad Max Fury Road", "anio": 2015, "rating": 8.1},
    ),
    "comedia": (
        {"titulo": "Superbad", "anio": 2007, "rating": 7.6},
        {"titulo": "The Hangover", "anio": 2009, "rating": 7.7},
    ),
}

__all__ = [
    "API_KEY_QUERY",
    "API_SUCCESS_RESPONSE",
    "DEFAULT_DELAY_SECONDS",
    "DISPLAY_WIDTH",
    "JSON_EXTENSION",
    "MENU_EXIT_OPTION",
    "MOVIES_BY_GENRE",
    "OMDB_MOVIE_TYPE_QUERY",
    "OMDB_SEARCH_BY_ACTOR_PATH",
    "OMDB_SEARCH_BY_TITLE_PATH",
    "POPULAR_MOVIES",
    "SEPARATOR_CHARACTER",
    "TVMAZE_SEARCH_SHOWS_PATH",
    "TVMAZE_SHOW_DETAILS_PATH",
]
