import os
import json
import time
from datetime import datetime
from typing import Any

# Variables globales
PROXY_CONFIG_FILE = "proxy_config.json"
proxy_config = {}

def load_proxy_config() -> None:
    """Carga configuración de proxy"""
    global proxy_config
    
    if os.path.exists(PROXY_CONFIG_FILE):
        with open(PROXY_CONFIG_FILE, 'r') as f:
            proxy_config = json.load(f)
        proxy_config.pop("password", None)  # Fase 5: nunca desde disco
    else:
        proxy_config = {
            "enabled": False,
            "host": "",
            "port": 8080,
            "username": ""
        }

def _strip_secrets(config: dict) -> dict:
    """Devuelve copia sin secretos para persistir o exportar."""
    safe = dict(config)
    safe.pop("password", None)
    return safe

def save_proxy_config() -> None:
    """Guarda configuración de proxy (sin secretos)"""
    with open(PROXY_CONFIG_FILE, 'w') as f:
        json.dump(_strip_secrets(proxy_config), f, indent=4)

def get_proxy_setting(key: str) -> Any:
    """Obtiene configuración de proxy"""
    return proxy_config.get(key)

def set_proxy_setting(key: str, value: Any) -> None:
    """Establece configuración de proxy"""
    proxy_config[key] = value
    save_proxy_config()

def get_all_proxy_settings() -> dict[str, Any]:
    """Obtiene todas las configuraciones de proxy"""
    return proxy_config.copy()

def reset_proxy_config() -> None:
    """Resetea configuración de proxy"""
    global proxy_config
    proxy_config = {
        "enabled": False,
        "host": "",
        "port": 8080,
        "username": ""
    }
    save_proxy_config()

def is_proxy_enabled() -> bool:
    """Verifica si proxy está habilitado"""
    return proxy_config.get("enabled", False)

def enable_proxy() -> None:
    """Habilita proxy"""
    proxy_config["enabled"] = True
    save_proxy_config()

def disable_proxy() -> None:
    """Deshabilita proxy"""
    proxy_config["enabled"] = False
    save_proxy_config()

def get_proxy_host() -> str:
    """Obtiene host de proxy"""
    return proxy_config.get("host", "")

def set_proxy_host(host: str) -> None:
    """Establece host de proxy"""
    proxy_config["host"] = host
    save_proxy_config()

def get_proxy_port() -> int:
    """Obtiene puerto de proxy"""
    return proxy_config.get("port", 8080)

def set_proxy_port(port: int) -> None:
    """Establece puerto de proxy"""
    proxy_config["port"] = port
    save_proxy_config()

def get_proxy_username() -> str:
    """Obtiene usuario de proxy"""
    return proxy_config.get("username", "")

def set_proxy_username(username: str) -> None:
    """Establece usuario de proxy"""
    proxy_config["username"] = username
    save_proxy_config()

def get_proxy_password() -> str:
    """Obtiene contraseña de proxy SOLO desde el entorno (PROXY_PASSWORD)"""
    return os.getenv("PROXY_PASSWORD", "")

def set_proxy_password(password: str) -> None:
    """Obsoleto: las contrasenas ya no se guardan en JSON. Usa PROXY_PASSWORD."""
    raise RuntimeError(
        "Por seguridad, la contrasena no se almacena en JSON. "
        "Define la variable de entorno PROXY_PASSWORD."
    )

def export_proxy_config(filename: str) -> None:
    """Exporta configuración de proxy (sin secretos)"""
    with open(filename, 'w') as f:
        json.dump(_strip_secrets(proxy_config), f, indent=4)

def import_proxy_config(filename: str) -> bool:
    """Importa configuración de proxy"""
    global proxy_config
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            proxy_config = json.load(f)
        save_proxy_config()
        return True
    return False

def validate_proxy_config() -> list[str]:
    """Valida configuración de proxy"""
    errors = []
    
    if "port" in proxy_config:
        if not isinstance(proxy_config["port"], int):
            errors.append("port must be integer")
    
    return errors

def backup_proxy_config() -> str:
    """Crea backup de configuración de proxy"""
    backup_name = f"proxy_config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_proxy_config(backup_name)
    return backup_name

def restore_proxy_config(backup_name: str) -> bool:
    """Restaura configuración de proxy desde backup"""
    return import_proxy_config(backup_name)

def get_proxy_config_summary() -> dict[str, Any]:
    """Obtiene resumen de configuración de proxy"""
    return {
        "enabled": is_proxy_enabled(),
        "host": get_proxy_host(),
        "port": get_proxy_port()
    }

# Cargar configuración de proxy al importar
load_proxy_config()
