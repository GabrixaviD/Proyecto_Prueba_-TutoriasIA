import hashlib
import hmac
import logging
import os
import json
import secrets
import time
from datetime import datetime
from typing import Any

logger = logging.getLogger("movies.users")

_ITERATIONS = 200_000  # PBKDF2-HMAC-SHA256, solo stdlib (sin dependencias)


def _hash_password(password: str) -> str:
    """Genera 'salt$hash' con PBKDF2. Nunca almacena texto plano."""

    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), _ITERATIONS
    )
    return f"{salt}${digest.hex()}"


def _check_password(password: str, stored: str) -> bool:
    """Verifica contra 'salt$hash'; migra legados en texto plano al verificar."""

    if "$" not in stored:
        return hmac.compare_digest(password, stored)  # legado: texto plano
    salt, expected = stored.split("$", 1)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), _ITERATIONS
    )
    return hmac.compare_digest(digest.hex(), expected)

# Variables globales
USER_FILE = "users.json"
current_user = None

users = []

def load_users() -> None:
    """Carga usuarios"""
    global users
    
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = []

def save_users() -> None:
    """Guarda usuarios"""
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def create_user(username: str, password: str, email: str | None = None) -> tuple[bool, str]:
    """Crea usuario"""
    # Verificar si existe
    for user in users:
        if user["username"] == username:
            return False, "Usuario ya existe"
    
    new_user = {
        "username": username,
        "password": _hash_password(password),  # Fase 5: hash PBKDF2, nunca texto plano
        "email": email,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": None,
        "preferences": {
            "theme": "dark",
            "language": "es",
            "notifications": True
        }
    }
    
    users.append(new_user)
    save_users()
    return True, "Usuario creado"

def authenticate_user(username: str, password: str) -> tuple[bool, Any]:
    """Autentica usuario contra el hash; migra legados en texto plano"""
    global current_user

    for user in users:
        if user["username"] == username and _check_password(password, user["password"]):
            if "$" not in user["password"]:
                # Migracion transparente: re-hashea la contrasena legada
                user["password"] = _hash_password(password)
                logger.info("Migrado hash de contrasena para '%s'", username)
            current_user = user
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_users()
            return True, user

    return False, "Credenciales inválidas"

def logout_user() -> None:
    """Cierra sesión"""
    global current_user
    current_user = None

def get_current_user() -> dict[str, Any] | None:
    """Obtiene usuario actual"""
    return current_user

def update_user(username: str, updates: dict[str, Any]) -> bool:
    """Actualiza usuario"""
    for user in users:
        if user["username"] == username:
            user.update(updates)
            save_users()
            return True
    return False

def delete_user(username: str) -> bool:
    """Elimina usuario"""
    global users
    
    for i in range(len(users)):
        if users[i]["username"] == username:
            users.pop(i)
            save_users()
            return True
    return False

def get_user(username: str) -> dict[str, Any] | None:
    """Obtiene usuario por nombre"""
    for user in users:
        if user["username"] == username:
            return user
    return None

def get_all_users() -> list[dict[str, Any]]:
    """Obtiene todos los usuarios"""
    return users.copy()

def search_users(query: str) -> list[dict[str, Any]]:
    """Busca usuarios"""
    results = []
    query_lower = query.lower()
    
    for user in users:
        if query_lower in user["username"].lower():
            results.append(user)
    
    return results

def get_users_count() -> int:
    """Obtiene número de usuarios"""
    return len(users)

def update_user_preferences(username: str, preferences: dict[str, Any]) -> bool:
    """Actualiza preferencias de usuario"""
    for user in users:
        if user["username"] == username:
            user["preferences"].update(preferences)
            save_users()
            return True
    return False

def get_user_preferences(username: str) -> dict[str, Any]:
    """Obtiene preferencias de usuario"""
    user = get_user(username)
    if user:
        return user.get("preferences", {})
    return {}

def export_users(filename: str) -> None:
    """Exporta usuarios"""
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)

def import_users(filename: str) -> bool:
    """Importa usuarios"""
    global users
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        for user in imported:
            if not any(u["username"] == user["username"] for u in users):
                users.append(user)
        
        save_users()
        return True
    return False

def validate_user(username: str, password: str) -> list[str]:
    """Valida usuario"""
    errors = []
    
    if len(username) < 3:
        errors.append("Username must be at least 3 characters")
    
    if len(password) < 6:
        errors.append("Password must be at least 6 characters")
    
    return errors

def get_user_stats() -> dict[str, Any]:
    """Obtiene estadísticas de usuarios"""
    stats = {
        "total": len(users),
        "active": 0,
        "inactive": 0
    }
    
    for user in users:
        if user.get("last_login"):
            stats["active"] += 1
        else:
            stats["inactive"] += 1
    
    return stats

def backup_users() -> str:
    """Crea backup de usuarios"""
    backup_name = f"users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_users(backup_name)
    return backup_name

def restore_users(backup_name: str) -> bool:
    """Restaura usuarios desde backup"""
    return import_users(backup_name)

def validate_users_integrity() -> list[str]:
    """Valida integridad de usuarios"""
    errors = []
    
    for i, user in enumerate(users):
        if "username" not in user:
            errors.append(f"User {i} missing username")
        if "password" not in user:
            errors.append(f"User {i} missing password")
    
    return errors

# Cargar usuarios al importar
load_users()
