import os
import json
import time
from datetime import datetime
from typing import Any

# Variables globales
EMAIL_CONFIG_FILE = "email_config.json"
email_config = {}

def load_email_config() -> None:
    """Carga configuración de email"""
    global email_config
    
    if os.path.exists(EMAIL_CONFIG_FILE):
        with open(EMAIL_CONFIG_FILE, 'r') as f:
            email_config = json.load(f)
        email_config.pop("sender_password", None)  # Fase 5: nunca desde disco
    else:
        email_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_tls": True,
            "sender_email": ""
        }

def _strip_secrets(config: dict) -> dict:
    """Devuelve copia sin secretos para persistir o exportar."""
    safe = dict(config)
    safe.pop("sender_password", None)
    return safe

def save_email_config() -> None:
    """Guarda configuración de email (sin secretos)"""
    with open(EMAIL_CONFIG_FILE, 'w') as f:
        json.dump(_strip_secrets(email_config), f, indent=4)

def get_email_setting(key: str) -> Any:
    """Obtiene configuración de email"""
    return email_config.get(key)

def set_email_setting(key: str, value: Any) -> None:
    """Establece configuración de email"""
    email_config[key] = value
    save_email_config()

def get_all_email_settings() -> dict[str, Any]:
    """Obtiene todas las configuraciones de email"""
    return email_config.copy()

def reset_email_config() -> None:
    """Resetea configuración de email"""
    global email_config
    email_config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": True,
        "sender_email": ""
    }
    save_email_config()

def get_smtp_server() -> str:
    """Obtiene servidor SMTP"""
    return email_config.get("smtp_server", "smtp.gmail.com")

def set_smtp_server(server: str) -> None:
    """Establece servidor SMTP"""
    email_config["smtp_server"] = server
    save_email_config()

def get_smtp_port() -> int:
    """Obtiene puerto SMTP"""
    return email_config.get("smtp_port", 587)

def set_smtp_port(port: int) -> None:
    """Establece puerto SMTP"""
    email_config["smtp_port"] = port
    save_email_config()

def is_tls_enabled() -> bool:
    """Verifica si TLS está habilitado"""
    return email_config.get("use_tls", True)

def enable_tls() -> None:
    """Habilita TLS"""
    email_config["use_tls"] = True
    save_email_config()

def disable_tls() -> None:
    """Deshabilita TLS"""
    email_config["use_tls"] = False
    save_email_config()

def get_sender_email() -> str:
    """Obtiene email del remitente"""
    return email_config.get("sender_email", "")

def set_sender_email(email: str) -> None:
    """Establece email del remitente"""
    email_config["sender_email"] = email
    save_email_config()

def get_sender_password() -> str:
    """Obtiene contraseña del remitente SOLO desde el entorno (SMTP_PASSWORD)"""
    return os.getenv("SMTP_PASSWORD", "")

def set_sender_password(password: str) -> None:
    """Obsoleto: las contrasenas ya no se guardan en JSON. Usa SMTP_PASSWORD."""
    raise RuntimeError(
        "Por seguridad, la contrasena no se almacena en JSON. "
        "Define la variable de entorno SMTP_PASSWORD."
    )

def export_email_config(filename: str) -> None:
    """Exporta configuración de email (sin secretos)"""
    with open(filename, 'w') as f:
        json.dump(_strip_secrets(email_config), f, indent=4)

def import_email_config(filename: str) -> bool:
    """Importa configuración de email"""
    global email_config
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            email_config = json.load(f)
        save_email_config()
        return True
    return False

def validate_email_config() -> list[str]:
    """Valida configuración de email"""
    errors = []
    
    if "smtp_port" in email_config:
        if not isinstance(email_config["smtp_port"], int):
            errors.append("smtp_port must be integer")
    
    return errors

def backup_email_config() -> str:
    """Crea backup de configuración de email"""
    backup_name = f"email_config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_email_config(backup_name)
    return backup_name

def restore_email_config(backup_name: str) -> bool:
    """Restaura configuración de email desde backup"""
    return import_email_config(backup_name)

def get_email_config_summary() -> dict[str, Any]:
    """Obtiene resumen de configuración de email"""
    return {
        "smtp_server": get_smtp_server(),
        "smtp_port": get_smtp_port(),
        "use_tls": is_tls_enabled()
    }

# Cargar configuración de email al importar
load_email_config()
