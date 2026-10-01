"""Logica del menu de consola: opciones y orquestacion (Fase 3)."""

import logging
import time
from typing import Any

from config import CONFIG
from exceptions import AppError
from constants import (
    DEFAULT_DELAY_SECONDS,
    JSON_EXTENSION,
    MENU_EXIT_OPTION,
)
from services.movie_service import (
    HISTORIAL_BUSQUEDAS,
    PELICULAS_FAVORITAS,
    agregar_a_favoritas,
    agregar_al_historial,
    buscar_pelicula,
    buscar_peliculas_por_actor,
    buscar_peliculas_por_genero,
    eliminar_de_favoritas,
    exportar_a_json,
    importar_de_json,
    limpiar_historial,
    obtener_estadisticas,
    obtener_peliculas_populares,
)
from services.series_service import buscar_series, obtener_detalles_serie
from ui.display import (
    clear_screen,
    mostrar_lista_peliculas,
    mostrar_pelicula,
    mostrar_serie,
    print_header,
)

logger = logging.getLogger("movies.ui.menu")


def delay(seconds: float) -> None:
    """Delay innecesario."""
    time.sleep(seconds)


def funcion_buscar_pelicula() -> None:
    """Busca pelicula."""
    titulo = input("Ingrese el título de la película: ")
    print("Buscando...")
    delay(DEFAULT_DELAY_SECONDS)  # Simular carga innecesaria

    pelicula = None
    try:
        pelicula = buscar_pelicula(titulo)
    except AppError as exc:
        logger.error("[%s] %s", exc.code, exc.message)
        print(f"Error [{exc.code}]: {exc.message}")
    mostrar_pelicula(pelicula)

    if pelicula is not None:
        agregar_al_historial(pelicula)
        opcion = input("\n¿Agregar a favoritos? (s/n): ")
        if opcion.lower() == "s":
            if agregar_a_favoritas(pelicula):
                print("¡Agregada a favoritos!")
            else:
                print("Ya está en favoritos")

    input("\nPresione Enter para continuar...")


def funcion_buscar_actor() -> None:
    """Busca actor."""
    actor = input("Ingrese el nombre del actor: ")
    print("Buscando películas del actor...")

    peliculas: list = []
    try:
        peliculas = buscar_peliculas_por_actor(actor)
    except AppError as exc:
        logger.error("[%s] %s", exc.code, exc.message)
        print(f"Error [{exc.code}]: {exc.message}")

    if len(peliculas) > 0:
        mostrar_lista_peliculas(peliculas)

        opcion = input(
            "\nSeleccione una película para ver detalles (0 para volver): "
        )
        if opcion.isdigit():
            indice = int(opcion) - 1
            if indice >= 0 and indice < len(peliculas):
                try:
                    detalles = buscar_pelicula(peliculas[indice]["Title"])
                except AppError as exc:
                    logger.error("[%s] %s", exc.code, exc.message)
                    print(f"Error [{exc.code}]: {exc.message}")
                    detalles = None
                mostrar_pelicula(detalles)
    else:
        print("No se encontraron películas para ese actor")

    input("\nPresione Enter para continuar...")


def funcion_buscar_series() -> None:
    """Busca series."""
    nombre = input("Ingrese el nombre de la serie: ")
    print("Buscando series...")

    series: list = []
    try:
        series = buscar_series(nombre)
    except AppError as exc:
        logger.error("[%s] %s", exc.code, exc.message)
        print(f"Error [{exc.code}]: {exc.message}")

    if len(series) > 0:
        i = 0
        while i < len(series):
            show = series[i].get("show", {})
            print(f"{i + 1}. {show.get('name', '')} ({show.get('status', '')})")
            i += 1

        opcion = input(
            "\nSeleccione una serie para ver detalles (0 para volver): "
        )
        if opcion.isdigit():
            indice = int(opcion) - 1
            if indice >= 0 and indice < len(series):
                try:
                    id_serie = series[indice].get("show", {}).get("id")
                    detalles = obtener_detalles_serie(id_serie)
                except AppError as exc:
                    logger.error("[%s] %s", exc.code, exc.message)
                    print(f"Error [{exc.code}]: {exc.message}")
                    detalles = None
                if detalles is not None:
                    mostrar_serie(detalles)
    else:
        print("No se encontraron series")

    input("\nPresione Enter para continuar...")


def funcion_peliculas_populares() -> None:
    """Muestra peliculas populares."""
    print_header("PELÍCULAS POPULARES")
    peliculas = obtener_peliculas_populares()
    mostrar_lista_peliculas(peliculas)
    input("\nPresione Enter para continuar...")


def funcion_buscar_por_genero() -> None:
    """Busca por genero."""
    print("Géneros disponibles: acción, comedia")
    genero = input("Ingrese el género: ")
    print("Buscando...")

    peliculas = buscar_peliculas_por_genero(genero)
    mostrar_lista_peliculas(peliculas)

    input("\nPresione Enter para continuar...")


def funcion_ver_favoritos() -> None:
    """Muestra favoritas."""
    print_header("MIS FAVORITOS")
    if len(PELICULAS_FAVORITAS) > 0:
        i = 0
        while i < len(PELICULAS_FAVORITAS):
            print(f"{i + 1}. {PELICULAS_FAVORITAS[i].get('Title', '')}")
            i += 1

        opcion = input(
            "\n¿Desea eliminar alguna? (número o Enter para volver): "
        )
        if opcion.isdigit():
            indice = int(opcion) - 1
            if indice >= 0 and indice < len(PELICULAS_FAVORITAS):
                titulo = PELICULAS_FAVORITAS[indice].get("Title")
                if eliminar_de_favoritas(titulo):
                    print("Eliminada de favoritos")
    else:
        print("No tienes películas favoritas")

    input("\nPresione Enter para continuar...")


def funcion_ver_historial() -> None:
    """Muestra historial."""
    print_header("HISTORIAL DE BÚSQUEDAS")
    if len(HISTORIAL_BUSQUEDAS) > 0:
        i = 0
        while i < len(HISTORIAL_BUSQUEDAS):
            print(f"{i + 1}. {HISTORIAL_BUSQUEDAS[i]['titulo']}")
            i += 1

        opcion = input("\n¿Limpiar historial? (s/n): ")
        if opcion.lower() == "s":
            limpiar_historial()
            print("Historial limpiado")
    else:
        print("No hay historial")

    input("\nPresione Enter para continuar...")


def funcion_estadisticas() -> None:
    """Muestra estadisticas."""
    print_header("ESTADÍSTICAS")
    stats = obtener_estadisticas()
    print(f"Total favoritas: {stats['total_favoritas']}")
    print(f"Total historial: {stats['total_historial']}")
    input("\nPresione Enter para continuar...")


def funcion_exportar() -> None:
    """Exporta datos."""
    nombre = input("Nombre del archivo (sin extensión): ")
    exportar_a_json(nombre + JSON_EXTENSION)
    input("\nPresione Enter para continuar...")


def funcion_importar() -> None:
    """Importa datos."""
    nombre = input("Nombre del archivo (sin extensión): ")
    try:
        importar_de_json(nombre + JSON_EXTENSION)
    except (OSError, ValueError) as exc:
        logger.error("Error al importar '%s': %s", nombre, exc)
        print(f"Error al importar archivo: {exc}")
    input("\nPresione Enter para continuar...")


def funcion_configuracion() -> None:
    """Configuracion."""
    print_header("CONFIGURACIÓN")
    print(f"1. Debug: {CONFIG.debug}")
    print(f"2. Verbose: {CONFIG.verbose}")
    print(f"3. Timeout: {CONFIG.api.timeout}")

    opcion = input("\nSeleccione opción a cambiar (0 para volver): ")
    if opcion == "1":
        CONFIG.debug = not CONFIG.debug
        print(f"Debug ahora es: {CONFIG.debug}")
    elif opcion == "2":
        CONFIG.verbose = not CONFIG.verbose
        print(f"Verbose ahora es: {CONFIG.verbose}")
    elif opcion == "3":
        CONFIG.api.timeout = int(input("Nuevo timeout: "))

    input("\nPresione Enter para continuar...")


def menu_principal() -> None:
    """Menu principal."""
    while True:
        clear_screen()
        print_header("SISTEMA DE PELÍCULAS Y SERIES")
        print("1. Buscar película por título")
        print("2. Buscar por actor")
        print("3. Buscar series")
        print("4. Ver películas populares")
        print("5. Buscar por género")
        print("6. Ver favoritos")
        print("7. Ver historial")
        print("8. Ver estadísticas")
        print("9. Exportar datos")
        print("10. Importar datos")
        print("11. Configuración")
        print("12. Salir")

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
            funcion_buscar_por_genero()
        elif opcion == "6":
            funcion_ver_favoritos()
        elif opcion == "7":
            funcion_ver_historial()
        elif opcion == "8":
            funcion_estadisticas()
        elif opcion == "9":
            funcion_exportar()
        elif opcion == "10":
            funcion_importar()
        elif opcion == "11":
            funcion_configuracion()
        elif opcion == MENU_EXIT_OPTION:
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")
            delay(1)


__all__ = [
    "delay",
    "funcion_buscar_actor",
    "funcion_buscar_pelicula",
    "funcion_buscar_por_genero",
    "funcion_buscar_series",
    "funcion_configuracion",
    "funcion_estadisticas",
    "funcion_exportar",
    "funcion_importar",
    "funcion_peliculas_populares",
    "funcion_ver_favoritos",
    "funcion_ver_historial",
    "menu_principal",
]
