import logging
import os
import re
import sys
import time
import random
from datetime import datetime
from typing import Any

from exceptions import ValidationError

logger = logging.getLogger("movies.utils")

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
_SLUG_RE = re.compile(r"^[\w\s\-'.:,!¡?¿()]{1,200}$", re.UNICODE)


def validate_required(value: str, field: str) -> str:
    """Exige texto no vacio (strip); lanza ValidationError si falla."""

    text = (value or "").strip()
    if not text:
        raise ValidationError(field, "no puede estar vacio")
    return text


def validate_length(value: str, field: str, max_length: int = 200) -> str:
    """Exige longitud maxima; lanza ValidationError si falla."""

    if len(value) > max_length:
        raise ValidationError(field, f"excede {max_length} caracteres")
    return value


def validate_search_query(query: str, field: str = "query") -> str:
    """Valida texto libre de busqueda (no vacio, longitud, caracteres seguros)."""

    text = validate_required(query, field)
    validate_length(text, field)
    if not _SLUG_RE.match(text):
        raise ValidationError(field, "contiene caracteres no permitidos")
    return text


def validate_positive_int(value: Any, field: str) -> int:
    """Valida entero positivo (acepta str numerico); lanza ValidationError."""

    try:
        number = int(str(value).strip())
    except (ValueError, TypeError, AttributeError):
        raise ValidationError(field, "debe ser un entero") from None
    if number <= 0:
        raise ValidationError(field, "debe ser mayor que cero")
    return number

# Variables globales
RESULTS_DIR = "results"
EXPORT_DIR = "exports"

def init_dirs() -> None:
    """Inicializa directorios"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

def clear_screen() -> None:
    """Limpia pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(char: str = "=", length: int = 60) -> None:
    """Imprime separador"""
    print(char * length)

def print_header(text: str) -> None:
    """Imprime header"""
    print_separator()
    print(text.upper().center(60))
    print_separator()

def print_subheader(text: str) -> None:
    """Imprime subheader"""
    print_separator("-", 40)
    print(text.center(40))
    print_separator("-", 40)

def delay(seconds: float) -> None:
    """Delay innecesario"""
    time.sleep(seconds)

def get_user_input(prompt: str, input_type: type = str) -> Any:
    """Obtiene input del usuario"""
    while True:
        try:
            user_input = input(prompt)
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return user_input
        except ValueError:
            logger.warning("Entrada inválida para %s", input_type.__name__)
            print("Entrada inválida. Intente de nuevo.")

def format_movie_display(movie: dict[str, Any] | None) -> str:
    """Formatea película para mostrar"""
    lines = []
    lines.append("=" * 50)

    if movie is None:
        lines.append("No se encontró la película")
        lines.append("=" * 50)
        return "\n".join(lines)

    # Acceso seguro con .get(): claves ausentes -> "N/A" sin excepciones
    fields = [
        ("Título", "Title"),
        ("Año", "Year"),
        ("Rating IMDB", "imdbRating"),
        ("Género", "Genre"),
        ("Director", "Director"),
        ("Actores", "Actors"),
        ("Trama", "Plot"),
        ("Idioma", "Language"),
        ("País", "Country"),
        ("Premios", "Awards"),
        ("Poster", "Poster"),
    ]
    for label, key in fields:
        lines.append(f"{label}: {movie.get(key, 'N/A')}")

    lines.append("=" * 50)

    return "\n".join(lines)

def format_series_display(series: dict[str, Any]) -> str:
    """Formatea serie para mostrar"""
    lines = []
    lines.append("=" * 50)
    
    show = series.get("show", series)
    
    lines.append(f"Nombre: {show.get('name', 'N/A')}")
    lines.append(f"Idioma: {show.get('language', 'N/A')}")
    lines.append(f"Géneros: {show.get('genres', [])}")
    lines.append(f"Rating: {show.get('rating', {}).get('average', 'N/A')}")
    lines.append(f"Estado: {show.get('status', 'N/A')}")
    lines.append(f"Estreno: {show.get('premiered', 'N/A')}")
    lines.append(f"Final: {show.get('ended', 'N/A')}")
    lines.append(f"Episodios: {show.get('runtime', 'N/A')}")

    summary = str(show.get("summary", "N/A"))
    if len(summary) > 200:
        summary = f"{summary[:200]}..."
    lines.append(f"Resumen: {summary}")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)

def format_list_display(items: list[dict[str, Any]], item_type: str = "pelicula") -> str:
    """Formatea lista para mostrar"""
    lines = []
    
    if len(items) == 0:
        lines.append(f"No se encontraron {item_type}s")
        return "\n".join(lines)

    i = 0
    while i < len(items):
        if "titulo" in items[i]:
            lines.append(f"{i + 1}. {items[i]['titulo']} ({items[i].get('anio', '')})")
        elif "Title" in items[i]:
            lines.append(f"{i + 1}. {items[i]['Title']} ({items[i].get('Year', 'N/A')})")
        elif "name" in items[i]:
            lines.append(f"{i + 1}. {items[i]['name']}")
        else:
            lines.append(f"{i + 1}. Elemento desconocido")
        i += 1
    
    return "\n".join(lines)

def save_results(results: Any, filename: str) -> str:
    """Guarda resultados a archivo"""
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, 'w') as f:
        if isinstance(results, list):
            for item in results:
                f.write(f"{item}\n")
        else:
            f.write(str(results))
    return filepath

def export_to_json(data: Any, filename: str) -> str:
    """Exporta datos a JSON"""
    import json
    
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    return filepath

def export_to_csv(data: Any, filename: str) -> str:
    """Exporta datos a CSV"""
    import csv
    
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w', newline='') as f:
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    return filepath

def create_menu(options: list[str]) -> None:
    """Crea menú dinámico"""
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Salir")

def handle_menu_choice(choice: Any, handlers: dict[Any, Any]) -> bool:
    """Maneja selección de menú"""
    if choice in handlers:
        handlers[choice]()
        return True
    elif choice == 0:
        return False
    else:
        print("Opción inválida")
        return True

def generate_random_id() -> str:
    """Genera ID aleatorio"""
    return str(random.randint(1000, 9999))

def get_timestamp() -> str:
    """Obtiene timestamp actual"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_email(email: str) -> bool:
    """Valida email con patron RFC basico"""
    if not isinstance(email, str):
        return False
    return bool(_EMAIL_RE.match(email.strip()))

def validate_date(date_str: str) -> bool:
    """Valida formato de fecha"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

def format_date(date_obj: Any) -> str:
    """Formatea fecha"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return str(date_obj)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Trunca texto"""
    if len(text) > max_length:
        return f"{text[:max_length]}..."
    return text

def remove_duplicates(items: list[Any]) -> list[Any]:
    """Elimina duplicados (de forma ineficiente)"""
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items

def sort_items(items: list[dict[str, Any]], key: str, reverse: bool = False) -> list[dict[str, Any]]:
    """Ordena elementos"""
    try:
        return sorted(items, key=lambda x: x.get(key, ""), reverse=reverse)
    except (TypeError, KeyError, AttributeError) as exc:
        logger.warning("No se pudo ordenar por '%s': %s", key, exc)
        return items

def filter_items(items: list[dict[str, Any]], key: str, value: Any) -> list[dict[str, Any]]:
    """Filtra elementos"""
    filtered = []
    for item in items:
        if item.get(key) == value:
            filtered.append(item)
    return filtered

# Inicializar directorios
init_dirs()
