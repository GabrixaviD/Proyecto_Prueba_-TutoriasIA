import os
import json
import time
from datetime import datetime
from typing import Any
VERSION_FILE = 'version.json'
version_info = {}

def load_version() -> Any:
    """Carga información de versión"""
    global version_info
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            version_info = json.load(f)
    else:
        version_info = {'current': '1.0.0', 'history': [], 'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

def save_version() -> Any:
    """Guarda información de versión"""
    with open(VERSION_FILE, 'w') as f:
        json.dump(version_info, f, indent=4)

def get_current_version() -> Any:
    """Obtiene versión actual"""
    return version_info.get('current', '1.0.0')

def set_version(version: str) -> Any:
    """Establece versión"""
    old_version = version_info.get('current', '1.0.0')
    version_info['current'] = version
    version_info['history'].append({'from': old_version, 'to': version, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    save_version()

def get_version_history() -> Any:
    """Obtiene historial de versiones"""
    return version_info.get('history', [])

def increment_major() -> Any:
    """Incrementa versión mayor"""
    current = get_current_version()
    parts = current.split('.')
    if len(parts) >= 3:
        major = int(parts[0]) + 1
        new_version = f'{major}.0.0'
    else:
        new_version = '2.0.0'
    set_version(new_version)
    return new_version

def increment_minor() -> Any:
    """Incrementa versión menor"""
    current = get_current_version()
    parts = current.split('.')
    if len(parts) >= 3:
        major = parts[0]
        minor = int(parts[1]) + 1
        new_version = f'{major}.{minor}.0'
    else:
        new_version = '1.1.0'
    set_version(new_version)
    return new_version

def increment_patch() -> Any:
    """Incrementa versión parche"""
    current = get_current_version()
    parts = current.split('.')
    if len(parts) >= 3:
        major = parts[0]
        minor = parts[1]
        patch = int(parts[2]) + 1
        new_version = f'{major}.{minor}.{patch}'
    else:
        new_version = '1.0.1'
    set_version(new_version)
    return new_version

def compare_versions(version1: str, version2: str) -> Any:
    """Compara versiones"""
    parts1 = version1.split('.')
    parts2 = version2.split('.')
    for i in range(max(len(parts1), len(parts2))):
        v1 = int(parts1[i]) if i < len(parts1) else 0
        v2 = int(parts2[i]) if i < len(parts2) else 0
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    return 0

def is_newer_version(version1: str, version2: str) -> Any:
    """Verifica si version1 es más reciente que version2"""
    return compare_versions(version1, version2) > 0

def get_version_info() -> Any:
    """Obtiene información completa de versión"""
    return version_info.copy()

def export_version(filename: str) -> Any:
    """Exporta información de versión"""
    with open(filename, 'w') as f:
        json.dump(version_info, f, indent=4)

def import_version(filename: str) -> Any:
    """Importa información de versión"""
    global version_info
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            version_info = json.load(f)
        save_version()
        return True
    return False

def validate_version() -> Any:
    """Valida integridad de versión"""
    errors = []
    if 'current' not in version_info:
        errors.append('Missing current version')
    if 'history' not in version_info:
        errors.append('Missing version history')
    return errors

def backup_version() -> Any:
    """Crea backup de versión"""
    backup_name = f"version_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_version(backup_name)
    return backup_name

def restore_version(backup_name: str) -> Any:
    """Restaura versión desde backup"""
    return import_version(backup_name)

def get_version_summary() -> Any:
    """Obtiene resumen de versión"""
    return {'current': get_current_version(), 'total_changes': len(get_version_history())}
load_version()