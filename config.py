"""Configuracion central de la aplicacion.

Este modulo reemplaza la configuracion dispersa en los archivos ``*_config.py``.
No lee ni escribe archivos al importarse; la persistencia es explicita mediante
``load_config`` y ``save_config``.
"""

from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()  # Carga .env local sin sobrescribir variables ya exportadas
except ImportError:  # pragma: no cover - python-dotenv es opcional
    pass

from exceptions import ConfigError


@dataclass
class ApiConfig:
    """Configuracion de los servicios externos."""

    omdb_key: str = ""  # Sin default: debe venir de OMDB_API_KEY (Fase 5)
    omdb_url: str = "http://www.omdbapi.com/"
    tvmaze_url: str = "http://api.tvmaze.com"
    timeout: int = 30
    max_retries: int = 3


@dataclass
class CacheConfig:
    """Configuracion de la cache local."""

    enabled: bool = True
    expiry_hours: int = 24
    max_size_mb: int = 100
    directory: str = "cache"


@dataclass
class UiConfig:
    """Preferencias de la interfaz de consola."""

    language: str = "es"
    theme: str = "dark"
    items_per_page: int = 10
    animations: bool = True


@dataclass
class LoggingConfig:
    """Configuracion del registro de eventos."""

    enabled: bool = True
    level: str = "DEBUG"
    file: str = "app.log"
    max_size_mb: int = 10


@dataclass
class PathsConfig:
    """Directorios usados para datos generados por la aplicacion."""

    results: str = "results"
    exports: str = "exports"
    data: str = "data"
    backups: str = "backups"


@dataclass
class AppConfig:
    """Configuracion completa de Peliculas y Series."""

    app_name: str = "Mi App de Peliculas"
    version: str = "1.0.0"
    debug: bool = True
    verbose: bool = True
    api: ApiConfig = field(default_factory=ApiConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    ui: UiConfig = field(default_factory=UiConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)


def _env_bool(name: str, default: bool) -> bool:
    """Lee un booleano desde el entorno conservando su valor por defecto."""

    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "si", "on"}


def _env_int(name: str, default: int) -> int:
    """Lee un entero desde el entorno y usa el defecto si no es valido."""

    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def default_config() -> AppConfig:
    """Construye la configuracion por defecto, incluyendo variables de entorno."""

    config = AppConfig()
    config.debug = _env_bool("MOVIES_DEBUG", config.debug)
    config.verbose = _env_bool("MOVIES_VERBOSE", config.verbose)
    config.api.omdb_key = os.getenv("OMDB_API_KEY", "")
    config.api.timeout = _env_int("MOVIES_API_TIMEOUT", config.api.timeout)
    config.api.max_retries = _env_int("MOVIES_MAX_RETRIES", config.api.max_retries)
    return config


def require_api_key(config: AppConfig | None = None) -> str:
    """Devuelve la API key o lanza ConfigError con instrucciones claras."""

    key = (config or CONFIG).api.omdb_key
    if not key:
        raise ConfigError(
            "Falta OMDB_API_KEY: exporta la variable de entorno "
            "o definela en un archivo .env (ver .env.example)"
        )
    return key


def _merge_config(config: AppConfig, values: dict[str, Any]) -> AppConfig:
    """Aplica valores JSON conocidos sin aceptar secciones arbitrarias."""

    for name, value in values.items():
        target = getattr(config, name, None)
        if isinstance(value, dict) and target is not None:
            for key, item in value.items():
                if hasattr(target, key):
                    setattr(target, key, item)
        elif hasattr(config, name):
            setattr(config, name, value)
    return config


def load_config(filename: str | Path = "config.json") -> AppConfig:
    """Carga configuracion desde JSON, combinandola con los valores por defecto."""

    config = default_config()
    path = Path(filename)
    if not path.exists():
        return config

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("La configuracion debe ser un objeto JSON")
    return _merge_config(config, data)


def save_config(config: AppConfig, filename: str | Path = "config.json") -> None:
    """Guarda una configuracion en formato JSON legible."""

    path = Path(filename)
    with path.open("w", encoding="utf-8") as file:
        json.dump(asdict(config), file, indent=4, ensure_ascii=False)


def get_config_value(config: AppConfig, path: str, default: Any = None) -> Any:
    """Obtiene un valor anidado usando una ruta como ``api.timeout``."""

    value: Any = config
    for part in path.split("."):
        if hasattr(value, part):
            value = getattr(value, part)
        else:
            return default
    return value


CONFIG = default_config()


__all__ = [
    "ApiConfig",
    "AppConfig",
    "CacheConfig",
    "CONFIG",
    "LoggingConfig",
    "PathsConfig",
    "UiConfig",
    "default_config",
    "get_config_value",
    "load_config",
    "require_api_key",
    "save_config",
]
