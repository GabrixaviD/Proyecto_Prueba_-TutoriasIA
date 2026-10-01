"""Tests de config central (Fases 2/5): env vars, require_api_key, persistencia."""

import json

import config
from config import default_config, load_config, require_api_key, save_config
from exceptions import ConfigError


def test_defaults_have_no_secrets():
    cfg = default_config()
    assert cfg.api.omdb_key == "" or isinstance(cfg.api.omdb_key, str)


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("OMDB_API_KEY", "env-key")
    monkeypatch.setenv("MOVIES_API_TIMEOUT", "10")
    monkeypatch.setenv("MOVIES_DEBUG", "si")
    cfg = default_config()
    assert cfg.api.omdb_key == "env-key"
    assert cfg.api.timeout == 10
    assert cfg.debug is True


def test_invalid_int_env_falls_back(monkeypatch):
    monkeypatch.setenv("MOVIES_API_TIMEOUT", "no-numero")
    assert default_config().api.timeout == 30


def test_require_api_key_ok(monkeypatch):
    monkeypatch.setenv("OMDB_API_KEY", "k")
    assert require_api_key(default_config()) == "k"


def test_require_api_key_missing_raises(monkeypatch):
    monkeypatch.delenv("OMDB_API_KEY", raising=False)
    cfg = default_config()
    cfg.api.omdb_key = ""
    try:
        require_api_key(cfg)
        raise AssertionError("debió lanzar ConfigError")
    except ConfigError as exc:
        assert exc.code == "CFG-4001"


def test_save_load_roundtrip(isolated_fs):
    cfg = default_config()
    cfg.app_name = "Test App"
    save_config(cfg, "config.json")
    loaded = load_config("config.json")
    assert loaded.app_name == "Test App"


def test_load_missing_file_returns_defaults(isolated_fs):
    assert load_config("no-existe.json").api.timeout == 30


def test_load_invalid_json_raises(isolated_fs):
    with open("config.json", "w", encoding="utf-8") as fh:
        json.dump(["no", "es", "dict"], fh)
    try:
        load_config("config.json")
        raise AssertionError("debió lanzar ValueError")
    except ValueError:
        pass


def test_get_config_value():
    cfg = default_config()
    assert config.get_config_value(cfg, "api.timeout") == cfg.api.timeout
    assert config.get_config_value(cfg, "no.existe", "dflt") == "dflt"
