import logging
import os
import json
import time
from datetime import datetime
from typing import Any

logger = logging.getLogger("movies.favorites")

# Variables globales
FAVORITES_FILE = "favorites.json"
favorites = []

def load_favorites() -> None:
    """Carga favoritas"""
    global favorites
    
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            favorites = json.load(f)
    else:
        favorites = []

def save_favorites() -> None:
    """Guarda favoritas"""
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=4)

def add_favorite(movie: dict[str, Any]) -> bool:
    """Agrega película a favoritas"""
    # Verificar duplicados
    exists = False
    for fav in favorites:
        if fav.get("Title") == movie.get("Title"):
            exists = True
            break
    
    if not exists:
        movie["added_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        favorites.append(movie)
        save_favorites()
        return True
    return False

def remove_favorite(title: str) -> bool:
    """Elimina película de favoritas"""
    for i in range(len(favorites)):
        if favorites[i].get("Title") == title:
            favorites.pop(i)
            save_favorites()
            return True
    return False

def get_favorites() -> list[dict[str, Any]]:
    """Obtiene todas las favoritas"""
    return favorites.copy()

def get_favorite(title: str) -> dict[str, Any] | None:
    """Obtiene favorita por título"""
    for fav in favorites:
        if fav.get("Title") == title:
            return fav
    return None

def search_favorites(query: str) -> list[dict[str, Any]]:
    """Busca en favoritas"""
    results = []
    query_lower = query.lower()
    
    for fav in favorites:
        title = fav.get("Title", "").lower()
        if query_lower in title:
            results.append(fav)
    
    return results

def sort_favorites(key: str, reverse: bool = False) -> list[dict[str, Any]]:
    """Ordena favoritas"""
    try:
        return sorted(favorites, key=lambda x: x.get(key, ""), reverse=reverse)
    except (TypeError, KeyError, AttributeError) as exc:
        logger.warning("No se pudo ordenar favoritas por '%s': %s", key, exc)
        return favorites.copy()

def get_favorites_count() -> int:
    """Obtiene número de favoritas"""
    return len(favorites)

def clear_favorites() -> None:
    """Limpia favoritas"""
    global favorites
    favorites = []
    save_favorites()

def export_favorites(filename: str) -> None:
    """Exporta favoritas"""
    with open(filename, 'w') as f:
        json.dump(favorites, f, indent=4)

def import_favorites(filename: str) -> bool:
    """Importa favoritas"""
    global favorites
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        for movie in imported:
            if not any(fav.get("Title") == movie.get("Title") for fav in favorites):
                favorites.append(movie)
        
        save_favorites()
        return True
    return False

def get_favorites_stats() -> dict[str, Any]:
    """Obtiene estadísticas de favoritas"""
    stats = {
        "total": len(favorites),
        "by_genre": {},
        "by_year": {},
        "avg_rating": 0
    }
    
    total_rating = 0
    rating_count = 0
    
    for fav in favorites:
        # Por género
        genre = fav.get("Genre", "Unknown")
        if isinstance(genre, str):
            genres = genre.split(", ")
            for g in genres:
                stats["by_genre"][g] = stats["by_genre"].get(g, 0) + 1
        
        # Por año
        year = fav.get("Year", "Unknown")
        stats["by_year"][year] = stats["by_year"].get(year, 0) + 1
        
        # Rating
        rating = fav.get("imdbRating")
        if rating and rating != "N/A":
            try:
                total_rating += float(rating)
                rating_count += 1
            except (ValueError, TypeError):
                continue
    
    if rating_count > 0:
        stats["avg_rating"] = total_rating / rating_count
    
    return stats

def get_recent_favorites(count: int = 10) -> list[dict[str, Any]]:
    """Obtiene favoritas recientes"""
    sorted_favs = sorted(favorites, key=lambda x: x.get("added_date", ""), reverse=True)
    return sorted_favs[:count]

def backup_favorites() -> str:
    """Crea backup de favoritas"""
    backup_name = f"favorites_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_favorites(backup_name)
    return backup_name

def restore_favorites(backup_name: str) -> bool:
    """Restaura favoritas desde backup"""
    return import_favorites(backup_name)

def validate_favorites() -> list[str]:
    """Valida integridad de favoritas"""
    errors = []
    
    for i, fav in enumerate(favorites):
        if "Title" not in fav:
            errors.append(f"Favorite {i} missing Title")
    
    return errors

def get_favorites_summary() -> dict[str, Any]:
    """Obtiene resumen de favoritas"""
    return {
        "total": len(favorites),
        "genres": list(set(fav.get("Genre", "") for fav in favorites if fav.get("Genre"))),
        "years": list(set(fav.get("Year", "") for fav in favorites if fav.get("Year")))
    }

# Cargar favoritas al importar
load_favorites()
