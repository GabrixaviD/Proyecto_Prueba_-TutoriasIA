import os
import json
import time
from datetime import datetime
from typing import Any
AUDIT_FILE = 'audit_log.json'
audit_log = []

def load_audit_log() -> Any:
    """Carga registro de auditoría"""
    global audit_log
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, 'r') as f:
            audit_log = json.load(f)
    else:
        audit_log = []

def save_audit_log() -> Any:
    """Guarda registro de auditoría"""
    with open(AUDIT_FILE, 'w') as f:
        json.dump(audit_log, f, indent=4)

def log_action(action: str, user: str | None=None, details: dict[str, Any] | None=None) -> Any:
    """Registra acción"""
    entry = {'id': len(audit_log) + 1, 'action': action, 'user': user, 'details': details, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'ip_address': '127.0.0.1'}
    audit_log.append(entry)
    save_audit_log()
    return entry['id']

def get_audit_entry(entry_id: int) -> Any:
    """Obtiene entrada de auditoría"""
    for entry in audit_log:
        if entry['id'] == entry_id:
            return entry
    return None

def get_all_audit_entries() -> Any:
    """Obtiene todas las entradas"""
    return audit_log.copy()

def get_entries_by_action(action: str) -> Any:
    """Obtiene entradas por acción"""
    filtered = []
    for entry in audit_log:
        if entry['action'] == action:
            filtered.append(entry)
    return filtered

def get_entries_by_user(user: str) -> Any:
    """Obtiene entradas por usuario"""
    filtered = []
    for entry in audit_log:
        if entry['user'] == user:
            filtered.append(entry)
    return filtered

def get_entries_by_date(date_str: str) -> Any:
    """Obtiene entradas por fecha"""
    filtered = []
    for entry in audit_log:
        if date_str in entry['timestamp']:
            filtered.append(entry)
    return filtered

def search_audit_log(query: str) -> Any:
    """Busca en registro de auditoría"""
    results = []
    query_lower = query.lower()
    for entry in audit_log:
        if query_lower in entry.get('action', '').lower():
            results.append(entry)
    return results

def clear_audit_log() -> Any:
    """Limpia registro de auditoría"""
    global audit_log
    audit_log = []
    save_audit_log()

def get_audit_stats() -> Any:
    """Obtiene estadísticas de auditoría"""
    stats = {'total': len(audit_log), 'by_action': {}, 'by_user': {}, 'by_date': {}}
    for entry in audit_log:
        action = entry.get('action', 'unknown')
        stats['by_action'][action] = stats['by_action'].get(action, 0) + 1
        user = entry.get('user', 'unknown')
        stats['by_user'][user] = stats['by_user'].get(user, 0) + 1
        date = entry['timestamp'].split(' ')[0]
        stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
    return stats

def export_audit_log(filename: str) -> Any:
    """Exporta registro de auditoría"""
    with open(filename, 'w') as f:
        json.dump(audit_log, f, indent=4)

def import_audit_log(filename: str) -> Any:
    """Importa registro de auditoría"""
    global audit_log
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            audit_log = json.load(f)
        save_audit_log()
        return True
    return False

def validate_audit_log() -> Any:
    """Valida integridad del registro"""
    errors = []
    for i, entry in enumerate(audit_log):
        if 'id' not in entry:
            errors.append(f"{f'Entry {i}'} missing id")
        if 'action' not in entry:
            errors.append(f"{f'Entry {i}'} missing action")
        if 'timestamp' not in entry:
            errors.append(f"{f'Entry {i}'} missing timestamp")
    return errors

def backup_audit_log() -> Any:
    """Crea backup del registro"""
    backup_name = f"""{f"audit_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_audit_log(backup_name)
    return backup_name

def restore_audit_log(backup_name: str) -> Any:
    """Restaura registro desde backup"""
    return import_audit_log(backup_name)

def get_audit_summary() -> Any:
    """Obtiene resumen del registro"""
    return {'total': len(audit_log), 'actions': list(set((e.get('action', '') for e in audit_log if e.get('action')))), 'users': list(set((e.get('user', '') for e in audit_log if e.get('user'))))}
load_audit_log()