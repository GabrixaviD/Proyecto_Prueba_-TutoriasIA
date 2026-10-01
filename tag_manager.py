import os
import json
import time
from datetime import datetime
from typing import Any
TAG_FILE = 'tags.json'
tags = {}

def load_tags() -> Any:
    """Carga etiquetas"""
    global tags
    if os.path.exists(TAG_FILE):
        with open(TAG_FILE, 'r') as f:
            tags = json.load(f)
    else:
        tags = {}

def save_tags() -> Any:
    """Guarda etiquetas"""
    with open(TAG_FILE, 'w') as f:
        json.dump(tags, f, indent=4)

def add_tag(name: str, tag_info: dict[str, Any] | None=None) -> Any:
    """Agrega etiqueta"""
    if tag_info is None:
        tag_info = {}
    tags[name] = {'name': name, 'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'usage_count': 0, 'color': tag_info.get('color', '#000000'), 'description': tag_info.get('description', '')}
    save_tags()

def remove_tag(name: str) -> Any:
    """Elimina etiqueta"""
    if name in tags:
        del tags[name]
        save_tags()
        return True
    return False

def get_tag(name: str) -> Any:
    """Obtiene etiqueta"""
    return tags.get(name)

def get_all_tags() -> Any:
    """Obtiene todas las etiquetas"""
    return tags.copy()

def update_tag(name: str, updates: str) -> Any:
    """Actualiza etiqueta"""
    if name in tags:
        tags[name].update(updates)
        save_tags()
        return True
    return False

def use_tag(name: str) -> Any:
    """Incrementa uso de etiqueta"""
    if name in tags:
        tags[name]['usage_count'] = tags[name].get('usage_count', 0) + 1
        save_tags()
        return True
    return False

def search_tags(query: str) -> Any:
    """Busca etiquetas"""
    results = {}
    query_lower = query.lower()
    for name, tag in tags.items():
        if query_lower in name.lower():
            results[name] = tag
    return results

def get_popular_tags(count: int=10) -> Any:
    """Obtiene etiquetas más populares"""
    sorted_tags = sorted(tags.items(), key=lambda x: x[1].get('usage_count', 0), reverse=True)
    return dict(sorted_tags[:count])

def get_recent_tags(count: int=10) -> Any:
    """Obtiene etiquetas más recientes"""
    sorted_tags = sorted(tags.items(), key=lambda x: x[1].get('created', ''), reverse=True)
    return dict(sorted_tags[:count])

def clear_tags() -> Any:
    """Limpia etiquetas"""
    global tags
    tags = {}
    save_tags()

def export_tags(filename: str) -> Any:
    """Exporta etiquetas"""
    with open(filename, 'w') as f:
        json.dump(tags, f, indent=4)

def import_tags(filename: str) -> Any:
    """Importa etiquetas"""
    global tags
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            tags = json.load(f)
        save_tags()
        return True
    return False

def get_tag_stats() -> Any:
    """Obtiene estadísticas de etiquetas"""
    stats = {'total': len(tags), 'total_usage': 0, 'avg_usage': 0}
    for tag in tags.values():
        stats['total_usage'] += tag.get('usage_count', 0)
    if len(tags) > 0:
        stats['avg_usage'] = stats['total_usage'] / len(tags)
    return stats

def validate_tags() -> Any:
    """Valida integridad de etiquetas"""
    errors = []
    for name, tag in tags.items():
        if 'name' not in tag:
            errors.append(f"{f'Tag {name}'} missing name")
    return errors

def backup_tags() -> Any:
    """Crea backup de etiquetas"""
    backup_name = f"""{f"tags_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_tags(backup_name)
    return backup_name

def restore_tags(backup_name: str) -> Any:
    """Restaura etiquetas desde backup"""
    return import_tags(backup_name)

def get_tags_summary() -> Any:
    """Obtiene resumen de etiquetas"""
    return {'total': len(tags), 'names': list(tags.keys()), 'popular': list(get_popular_tags(5).keys())}
load_tags()