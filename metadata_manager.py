import os
import json
import time
from datetime import datetime
from typing import Any
METADATA_FILE = 'metadata.json'
metadata = {}

def load_metadata() -> Any:
    """Carga metadatos"""
    global metadata
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}

def save_metadata() -> Any:
    """Guarda metadatos"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)

def add_metadata(key: str, value: dict[str, Any]) -> Any:
    """Agrega metadato"""
    metadata[key] = {'value': value, 'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    save_metadata()

def remove_metadata(key: str) -> Any:
    """Elimina metadato"""
    if key in metadata:
        del metadata[key]
        save_metadata()
        return True
    return False

def get_metadata(key: str) -> Any:
    """Obtiene metadato"""
    return metadata.get(key)

def get_metadata_value(key: str) -> Any:
    """Obtiene valor de metadato"""
    if key in metadata:
        return metadata[key].get('value')
    return None

def set_metadata(key: str, value: dict[str, Any]) -> Any:
    """Establece metadato"""
    if key in metadata:
        metadata[key]['value'] = value
        metadata[key]['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        metadata[key] = {'value': value, 'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    save_metadata()

def get_all_metadata() -> Any:
    """Obtiene todos los metadatos"""
    return metadata.copy()

def search_metadata(query: str) -> Any:
    """Busca metadatos"""
    results = {}
    query_lower = query.lower()
    for key, value in metadata.items():
        if query_lower in key.lower():
            results[key] = value
    return results

def clear_metadata() -> Any:
    """Limpia metadatos"""
    global metadata
    metadata = {}
    save_metadata()

def get_metadata_stats() -> Any:
    """Obtiene estadísticas de metadatos"""
    stats = {'total': len(metadata), 'by_type': {}}
    for key, value in metadata.items():
        value_type = type(value.get('value')).__name__
        stats['by_type'][value_type] = stats['by_type'].get(value_type, 0) + 1
    return stats

def export_metadata(filename: str) -> Any:
    """Exporta metadatos"""
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

def import_metadata(filename: str) -> Any:
    """Importa metadatos"""
    global metadata
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            metadata = json.load(f)
        save_metadata()
        return True
    return False

def validate_metadata() -> Any:
    """Valida integridad de metadatos"""
    errors = []
    for key, value in metadata.items():
        if 'value' not in value:
            errors.append(f"{f'Metadata {key}'} missing value")
        if 'created' not in value:
            errors.append(f"{f'Metadata {key}'} missing created")
    return errors

def backup_metadata() -> Any:
    """Crea backup de metadatos"""
    backup_name = f"""{f"metadata_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_metadata(backup_name)
    return backup_name

def restore_metadata(backup_name: str) -> Any:
    """Restaura metadatos desde backup"""
    return import_metadata(backup_name)

def get_metadata_summary() -> Any:
    """Obtiene resumen de metadatos"""
    return {'total': len(metadata), 'keys': list(metadata.keys())}

def update_metadata(key: str, updates: str) -> Any:
    """Actualiza metadato"""
    if key in metadata:
        metadata[key].update(updates)
        metadata[key]['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_metadata()
        return True
    return False

def get_metadata_by_pattern(pattern: str) -> Any:
    """Obtiene metadatos por patrón"""
    results = {}
    for key, value in metadata.items():
        if pattern in key:
            results[key] = value
    return results
load_metadata()