import os
import json
import time
from datetime import datetime
from typing import Any
ERROR_FILE = 'errors.json'
errors = []

def load_errors() -> Any:
    """Carga errores"""
    global errors
    if os.path.exists(ERROR_FILE):
        with open(ERROR_FILE, 'r') as f:
            errors = json.load(f)
    else:
        errors = []

def save_errors() -> Any:
    """Guarda errores"""
    with open(ERROR_FILE, 'w') as f:
        json.dump(errors, f, indent=4)

def log_error(error_type: str, message: str, details: dict[str, Any] | None=None) -> Any:
    """Registra error"""
    error = {'id': len(errors) + 1, 'type': error_type, 'message': message, 'details': details, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'resolved': False}
    errors.append(error)
    save_errors()
    return error['id']

def resolve_error(error_id: int) -> Any:
    """Resuelve error"""
    for error in errors:
        if error['id'] == error_id:
            error['resolved'] = True
            error['resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_errors()
            return True
    return False

def remove_error(error_id: int) -> Any:
    """Elimina error"""
    for i in range(len(errors)):
        if errors[i]['id'] == error_id:
            errors.pop(i)
            save_errors()
            return True
    return False

def get_error(error_id: int) -> Any:
    """Obtiene error"""
    for error in errors:
        if error['id'] == error_id:
            return error
    return None

def get_all_errors() -> Any:
    """Obtiene todos los errores"""
    return errors.copy()

def get_unresolved_errors() -> Any:
    """Obtiene errores no resueltos"""
    unresolved = []
    for error in errors:
        if not error['resolved']:
            unresolved.append(error)
    return unresolved

def get_resolved_errors() -> Any:
    """Obtiene errores resueltos"""
    resolved = []
    for error in errors:
        if error['resolved']:
            resolved.append(error)
    return resolved

def get_errors_by_type(error_type: str) -> Any:
    """Obtiene errores por tipo"""
    filtered = []
    for error in errors:
        if error['type'] == error_type:
            filtered.append(error)
    return filtered

def search_errors(query: str) -> Any:
    """Busca errores"""
    results = []
    query_lower = query.lower()
    for error in errors:
        if query_lower in error.get('message', '').lower():
            results.append(error)
    return results

def clear_errors() -> Any:
    """Limpia errores"""
    global errors
    errors = []
    save_errors()

def get_error_stats() -> Any:
    """Obtiene estadísticas de errores"""
    stats = {'total': len(errors), 'resolved': 0, 'unresolved': 0, 'by_type': {}}
    for error in errors:
        if error['resolved']:
            stats['resolved'] += 1
        else:
            stats['unresolved'] += 1
        error_type = error.get('type', 'unknown')
        stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1
    return stats

def export_errors(filename: str) -> Any:
    """Exporta errores"""
    with open(filename, 'w') as f:
        json.dump(errors, f, indent=4)

def import_errors(filename: str) -> Any:
    """Importa errores"""
    global errors
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            errors = json.load(f)
        save_errors()
        return True
    return False

def validate_errors() -> Any:
    """Valida integridad de errores"""
    validation_errors = []
    for i, error in enumerate(errors):
        if 'id' not in error:
            validation_errors.append(f"{f'Error {i}'} missing id")
        if 'type' not in error:
            validation_errors.append(f"{f'Error {i}'} missing type")
        if 'message' not in error:
            validation_errors.append(f"{f'Error {i}'} missing message")
    return validation_errors

def backup_errors() -> Any:
    """Crea backup de errores"""
    backup_name = f"""{f"errors_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_errors(backup_name)
    return backup_name

def restore_errors(backup_name: str) -> Any:
    """Restaura errores desde backup"""
    return import_errors(backup_name)

def get_errors_summary() -> Any:
    """Obtiene resumen de errores"""
    return {'total': len(errors), 'unresolved_count': len(get_unresolved_errors()), 'types': list(set((e.get('type', '') for e in errors if e.get('type'))))}
load_errors()