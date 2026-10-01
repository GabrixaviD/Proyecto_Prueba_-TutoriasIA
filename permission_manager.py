import os
import json
import time
from datetime import datetime
from typing import Any
PERMISSION_FILE = 'permissions.json'
permissions = {}

def load_permissions() -> Any:
    """Carga permisos"""
    global permissions
    if os.path.exists(PERMISSION_FILE):
        with open(PERMISSION_FILE, 'r') as f:
            permissions = json.load(f)
    else:
        permissions = {}

def save_permissions() -> Any:
    """Guarda permisos"""
    with open(PERMISSION_FILE, 'w') as f:
        json.dump(permissions, f, indent=4)

def add_permission(role: str, permission_list: str) -> Any:
    """Agrega permisos a un rol"""
    permissions[role] = {'role': role, 'permissions': permission_list, 'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    save_permissions()

def remove_permission(role: str) -> Any:
    """Elimina permisos de un rol"""
    if role in permissions:
        del permissions[role]
        save_permissions()
        return True
    return False

def get_permission(role: str) -> Any:
    """Obtiene permisos de un rol"""
    return permissions.get(role)

def get_all_permissions() -> Any:
    """Obtiene todos los permisos"""
    return permissions.copy()

def add_role_permission(role: str, permission: str) -> Any:
    """Agrega un permiso a un rol"""
    if role in permissions:
        if permission not in permissions[role]['permissions']:
            permissions[role]['permissions'].append(permission)
            save_permissions()
            return True
    return False

def remove_role_permission(role: str, permission: str) -> Any:
    """Elimina un permiso de un rol"""
    if role in permissions:
        if permission in permissions[role]['permissions']:
            permissions[role]['permissions'].remove(permission)
            save_permissions()
            return True
    return False

def has_permission(role: str, permission: str) -> Any:
    """Verifica si un rol tiene un permiso"""
    if role in permissions:
        return permission in permissions[role]['permissions']
    return False

def get_roles_with_permission(permission: str) -> Any:
    """Obtiene roles con un permiso específico"""
    roles = []
    for role, info in permissions.items():
        if permission in info['permissions']:
            roles.append(role)
    return roles

def search_permissions(query: str) -> Any:
    """Busca permisos"""
    results = {}
    query_lower = query.lower()
    for role, info in permissions.items():
        if query_lower in role.lower():
            results[role] = info
    return results

def clear_permissions() -> Any:
    """Limpia permisos"""
    global permissions
    permissions = {}
    save_permissions()

def get_permission_stats() -> Any:
    """Obtiene estadísticas de permisos"""
    stats = {'total_roles': len(permissions), 'total_permissions': 0, 'avg_permissions_per_role': 0}
    for info in permissions.values():
        stats['total_permissions'] += len(info.get('permissions', []))
    if len(permissions) > 0:
        stats['avg_permissions_per_role'] = stats['total_permissions'] / len(permissions)
    return stats

def export_permissions(filename: str) -> Any:
    """Exporta permisos"""
    with open(filename, 'w') as f:
        json.dump(permissions, f, indent=4)

def import_permissions(filename: str) -> Any:
    """Importa permisos"""
    global permissions
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            permissions = json.load(f)
        save_permissions()
        return True
    return False

def validate_permissions() -> Any:
    """Valida integridad de permisos"""
    errors = []
    for role, info in permissions.items():
        if 'role' not in info:
            errors.append(f"{f'Role {role}'} missing role field")
        if 'permissions' not in info:
            errors.append(f"{f'Role {role}'} missing permissions")
    return errors

def backup_permissions() -> Any:
    """Crea backup de permisos"""
    backup_name = f"""{f"permissions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_permissions(backup_name)
    return backup_name

def restore_permissions(backup_name: str) -> Any:
    """Restaura permisos desde backup"""
    return import_permissions(backup_name)

def get_permissions_summary() -> Any:
    """Obtiene resumen de permisos"""
    return {'total_roles': len(permissions), 'roles': list(permissions.keys())}
load_permissions()