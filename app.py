import logging
import requests
import json
import sys
import os
import time
import random

from log_setup import setup_logging
from typing import Any

setup_logging()
logger = logging.getLogger("movies.app")

# Variables globales
API_KEY = os.getenv("OMDB_API_KEY", "")  # Fase 5: sin secretos hardcodeados
OMDB_BASE_URL = "http://www.omdbapi.com/"
TVMAZE_BASE_URL = "http://api.tvmaze.com"
CACHE = {}
USUARIO_ACTUAL = None
PELICULAS_FAVORITAS = []
HISTORIAL = []

# Funciones de utilidad (mezcladas con lógica de negocio)
def print_sep() -> None:
    print("=" * 50)

def print_header(text: str) -> None:
    print_sep()
    print(text.upper())
    print_sep()

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds: float) -> None:
    time.sleep(seconds)

# Funciones de API (sin manejo de errores, sin logging, sin validación)
def buscar_pelicula_omdb(titulo: str) -> dict[str, Any] | None:
    global CACHE
    if titulo in CACHE:
        print("Usando cache...")
        return CACHE[titulo]
    
    url = f"{OMDB_BASE_URL}?t={titulo}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "True":
        CACHE[titulo] = data
        return data
    else:
        return None

def buscar_series_tvmaze(nombre: str) -> list[dict[str, Any]]:
    global CACHE
    cache_key = f"series_{nombre}"
    if cache_key in CACHE:
        print("Usando cache de series...")
        return CACHE[cache_key]
    
    url = f"{TVMAZE_BASE_URL}/search/shows?q={nombre}"
    response = requests.get(url)
    data = response.json()
    
    CACHE[cache_key] = data
    return data

def obtener_detalles_serie_tvmaze(id_serie: int) -> dict[str, Any]:
    url = f"{TVMAZE_BASE_URL}/shows/{id_serie}"
    response = requests.get(url)
    return response.json()

def buscar_peliculas_por_actor(nombre_actor: str) -> list[dict[str, Any]]:
    url = f"{OMDB_BASE_URL}?s={nombre_actor}&type=movie&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "True":
        return data.get("Search", [])
    return []

def obtener_peliculas_populares() -> list[dict[str, Any]]:
    # Simular películas populares con datos hardcodeados
    peliculas = [
        {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
        {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
        {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
        {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
        {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8}
    ]
    return peliculas

# Funciones de presentación (mezcladas con lógica)
def mostrar_pelicula(pelicula: dict[str, Any] | None) -> None:
    print_sep()
    if pelicula is None:
        print("No se encontró la película")
        return
    
    print(f"Título: {pelicula.get('Title', 'N/A')}")
    print(f"Año: {pelicula.get('Year', 'N/A')}")
    print(f"Rating: {pelicula.get('imdbRating', 'N/A')}")
    print(f"Género: {pelicula.get('Genre', 'N/A')}")
    print(f"Director: {pelicula.get('Director', 'N/A')}")
    print(f"Trama: {pelicula.get('Plot', 'N/A')}")
    print_sep()

def mostrar_serie(serie: dict[str, Any]) -> None:
    print_sep()
    show = serie.get("show", serie)
    print(f"Nombre: {show.get('name', 'N/A')}")
    print(f"Idioma: {show.get('language', 'N/A')}")
    print(f"Géneros: {show.get('genres', [])}")
    print(f"Rating: {show.get('rating', {}).get('average', 'N/A')}")
    print(f"Estado: {show.get('status', 'N/A')}")
    print_sep()

def mostrar_lista_peliculas(peliculas: list[dict[str, Any]]) -> None:
    i = 0
    while i < len(peliculas):
        print(f"{i + 1}. {peliculas[i].get('titulo', peliculas[i].get('Title', 'Sin título'))}")
        i += 1

# Funciones de menú
def menu_principal() -> None:
    while True:
        clear_screen()
        print_header("SISTEMA DE PELÍCULAS")
        print("1. Buscar película por título")
        print("2. Buscar por actor")
        print("3. Buscar series")
        print("4. Ver películas populares")
        print("5. Ver favoritos")
        print("6. Ver historial")
        print("7. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            funcion_buscar_pelicula()
        elif opcion == "2":
            funcion_buscar_actor()
        elif opcion == "3":
            funcion_buscar_series()
        elif opcion == "4":
            funcion_peliculas_populares()
        elif opcion == "5":
            funcion_ver_favoritos()
        elif opcion == "6":
            funcion_ver_historial()
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")
            delay(1)

def funcion_buscar_pelicula() -> None:
    titulo = input("Ingrese el título de la película: ")
    print("Buscando...")
    delay(1)  # Simular carga
    
    pelicula = buscar_pelicula_omdb(titulo)
    mostrar_pelicula(pelicula)
    
    if pelicula:
        HISTORIAL.append(pelicula.get("Title"))
        opcion = input("\n¿Agregar a favoritos? (s/n): ")
        if opcion.lower() == "s":
            PELICULAS_FAVORITAS.append(pelicula)
            print("Agregada a favoritos!")
    
    input("\nPresione Enter para continuar...")

def funcion_buscar_actor() -> None:
    actor = input("Ingrese el nombre del actor: ")
    print("Buscando películas del actor...")
    
    peliculas = buscar_peliculas_por_actor(actor)
    
    if len(peliculas) > 0:
        i = 0
        while i < len(peliculas):
            print(f"{i + 1}. {peliculas[i].get('Title', '')} ({peliculas[i].get('Year', '')})")
            i += 1
        
        opcion = input("\nSeleccione una película para ver detalles (0 para volver): ")
        if opcion.isdigit() and int(opcion) > 0:
            indice = int(opcion) - 1
            if indice < len(peliculas):
                detalles = buscar_pelicula_omdb(peliculas[indice].get("Title"))
                mostrar_pelicula(detalles)
    else:
        print("No se encontraron películas para ese actor")
    
    input("\nPresione Enter para continuar...")

def funcion_buscar_series() -> None:
    nombre = input("Ingrese el nombre de la serie: ")
    print("Buscando series...")
    
    series = buscar_series_tvmaze(nombre)
    
    if len(series) > 0:
        i = 0
        while i < len(series):
            show = series[i].get("show", {})
            print(f"{i + 1}. {show.get('name', '')} ({show.get('status', '')})")
            i += 1
        
        opcion = input("\nSeleccione una serie para ver detalles (0 para volver): ")
        if opcion.isdigit() and int(opcion) > 0:
            indice = int(opcion) - 1
            if indice < len(series):
                id_serie = series[indice].get("show", {}).get("id")
                detalles = obtener_detalles_serie_tvmaze(id_serie)
                mostrar_serie(detalles)
    else:
        print("No se encontraron series")
    
    input("\nPresione Enter para continuar...")

def funcion_peliculas_populares() -> None:
    print_header("PELÍCULAS POPULARES")
    peliculas = obtener_peliculas_populares()
    mostrar_lista_peliculas(peliculas)
    input("\nPresione Enter para continuar...")

def funcion_ver_favoritos() -> None:
    print_header("MIS FAVORITOS")
    if len(PELICULAS_FAVORITAS) > 0:
        i = 0
        while i < len(PELICULAS_FAVORITAS):
            print(f"{i + 1}. {PELICULAS_FAVORITAS[i].get('Title', '')}")
            i += 1
    else:
        print("No tienes películas favoritas")
    input("\nPresione Enter para continuar...")

def funcion_ver_historial() -> None:
    print_header("HISTORIAL DE BÚSQUEDAS")
    if len(HISTORIAL) > 0:
        i = 0
        while i < len(HISTORIAL):
            print(f"{i + 1}. {HISTORIAL[i]}")
            i += 1
    else:
        print("No hay historial")
    input("\nPresione Enter para continuar...")

# Programa principal
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except Exception as e:
        logger.exception("Error inesperado: %s", e)
        print(f"Error inesperado: {e}")
        sys.exit(1)
