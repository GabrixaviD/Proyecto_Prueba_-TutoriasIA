import json
import os
import csv
from datetime import datetime
from typing import Any

# Variables globales
DATA_DIR = "data"
BACKUP_DIR = "backups"
DATA_FILE = os.path.join(DATA_DIR, "datos.json")
BACKUP_FILE = os.path.join(BACKUP_DIR, "backup_{}.json")

def init_data_dir() -> Any:
    """Inicializa directorios de datos"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def load_data() -> Any:
    """Carga datos desde archivo"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"peliculas": [], "series": [], "favoritas": [], "historial": []}

def save_data(data: dict[str, Any]) -> Any:
    """Guarda datos a archivo"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_movie(movie_data: dict[str, Any]) -> Any:
    """Agrega película"""
    data = load_data()
    data["peliculas"].append(movie_data)
    save_data(data)

def add_series(series_data: dict[str, Any]) -> Any:
    """Agrega serie"""
    data = load_data()
    data["series"].append(series_data)
    save_data(data)

def add_favorite(favorite_data: dict[str, Any]) -> Any:
    """Agrega favorita"""
    data = load_data()
    data["favoritas"].append(favorite_data)
    save_data(data)

def remove_favorite(title: str) -> Any:
    """Elimina favorita"""
    data = load_data()
    new_favorites = []
    for fav in data["favoritas"]:
        if fav.get("titulo") != title and fav.get("Title") != title:
            new_favorites.append(fav)
    data["favoritas"] = new_favorites
    save_data(data)

def add_to_history(history_data: dict[str, Any]) -> Any:
    """Agrega al historial"""
    data = load_data()
    history_data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["historial"].append(history_data)
    save_data(data)

def clear_history() -> Any:
    """Limpia historial"""
    data = load_data()
    data["historial"] = []
    save_data(data)

def get_all_movies() -> Any:
    """Obtiene todas las películas"""
    data = load_data()
    return data.get("peliculas", [])

def get_all_series() -> Any:
    """Obtiene todas las series"""
    data = load_data()
    return data.get("series", [])

def get_all_favorites() -> Any:
    """Obtiene todas las favoritas"""
    data = load_data()
    return data.get("favoritas", [])

def get_history() -> Any:
    """Obtiene historial"""
    data = load_data()
    return data.get("historial", [])

def search_movies(query: str) -> Any:
    """Busca películas por título"""
    movies = get_all_movies()
    results = []
    query_lower = query.lower()
    
    for movie in movies:
        title = movie.get("titulo", movie.get("Title", "")).lower()
        if query_lower in title:
            results.append(movie)
    
    return results

def search_series(query: str) -> Any:
    """Busca series por nombre"""
    series = get_all_series()
    results = []
    query_lower = query.lower()
    
    for s in series:
        name = s.get("nombre", s.get("name", "")).lower()
        if query_lower in name:
            results.append(s)
    
    return results

def create_backup() -> Any:
    """Crea backup de datos"""
    data = load_data()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = BACKUP_FILE.format(timestamp)
    
    with open(backup_filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return backup_filename

def restore_backup(backup_file: str) -> Any:
    """Restaura backup"""
    if os.path.exists(backup_file):
        with open(backup_file, 'r') as f:
            data = json.load(f)
        save_data(data)
        return True
    return False

def list_backups() -> Any:
    """Lista backups disponibles"""
    backups = []
    if os.path.exists(BACKUP_DIR):
        for filename in os.listdir(BACKUP_DIR):
            if filename.endswith(".json"):
                backups.append(filename)
    return backups

def export_to_csv(filename: str) -> Any:
    """Exporta datos a CSV"""
    data = load_data()
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Encabezados
        writer.writerow(["Tipo", "Título", "Año", "Rating", "Género"])
        
        # Películas
        for movie in data.get("peliculas", []):
            writer.writerow([
                "Película",
                movie.get("titulo", movie.get("Title", "")),
                movie.get("anio", movie.get("Year", "")),
                movie.get("rating", movie.get("imdbRating", "")),
                movie.get("genero", movie.get("Genre", ""))
            ])
        
        # Series
        for series in data.get("series", []):
            writer.writerow([
                "Serie",
                series.get("nombre", series.get("name", "")),
                "",
                series.get("rating", ""),
                series.get("genero", "")
            ])

def import_from_csv(filename: str) -> Any:
    """Importa datos desde CSV"""
    data = load_data()
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row["Tipo"] == "Película":
                movie = {
                    "titulo": row["Título"],
                    "anio": row["Año"],
                    "rating": row["Rating"],
                    "genero": row["Género"]
                }
                data["peliculas"].append(movie)
            elif row["Tipo"] == "Serie":
                series = {
                    "nombre": row["Título"],
                    "rating": row["Rating"],
                    "genero": row["Género"]
                }
                data["series"].append(series)
    
    save_data(data)

def get_stats() -> Any:
    """Obtiene estadísticas de datos"""
    data = load_data()
    
    return {
        "total_peliculas": len(data.get("peliculas", [])),
        "total_series": len(data.get("series", [])),
        "total_favoritas": len(data.get("favoritas", [])),
        "total_historial": len(data.get("historial", []))
    }

def clear_all_data() -> Any:
    """Limpia todos los datos"""
    data = {
        "peliculas": [],
        "series": [],
        "favoritas": [],
        "historial": []
    }
    save_data(data)

def delete_data_file() -> Any:
    """Elimina archivo de datos"""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def get_data_size() -> Any:
    """Obtiene tamaño del archivo de datos"""
    if os.path.exists(DATA_FILE):
        return os.path.getsize(DATA_FILE)
    return 0

def validate_data() -> Any:
    """Valida integridad de datos"""
    data = load_data()
    errors = []
    
    required_keys = ["peliculas", "series", "favoritas", "historial"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Falta clave: {key}")
        elif not isinstance(data[key], list):
            errors.append(f"Clave {key} no es lista")
    
    return errors

# Inicializar directorios
init_data_dir()
