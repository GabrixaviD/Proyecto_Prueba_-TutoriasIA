"""Tests de log_setup, email_config y proxy_config (Fases 4/5)."""

import json
import logging

import email_config
import log_setup
import proxy_config
from log_setup import get_logger, setup_logging


def test_setup_logging_idempotent_and_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    first = setup_logging(level="DEBUG", log_file="test.log")
    second = setup_logging()
    assert first is second
    first.info("hola-log")
    for handler in first.handlers:
        handler.flush()
    assert "hola-log" in (tmp_path / "test.log").read_text(encoding="utf-8")


def test_get_logger_returns_child():
    logger = get_logger("movies.test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "movies.test"


def test_smtp_password_only_from_env(monkeypatch):
    monkeypatch.setenv("SMTP_PASSWORD", "abc123")
    assert email_config.get_sender_password() == "abc123"
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    assert email_config.get_sender_password() == ""


def test_smtp_setter_blocked():
    try:
        email_config.set_sender_password("x")
        raise AssertionError("debió lanzar RuntimeError")
    except RuntimeError as exc:
        assert "SMTP_PASSWORD" in str(exc)


def test_email_save_never_persists_password(isolated_fs, monkeypatch):
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    email_config.email_config = {"sender_email": "a@b.com",
                                 "sender_password": "LEGADO"}
    email_config.save_email_config()
    saved = json.loads(open("email_config.json", encoding="utf-8").read())
    assert "sender_password" not in saved
    assert email_config.export_email_config("out.json") is None
    assert "sender_password" not in json.loads(
        open("out.json", encoding="utf-8").read())


def test_email_load_purges_legacy_password(isolated_fs):
    with open("email_config.json", "w", encoding="utf-8") as fh:
        json.dump({"sender_email": "a@b.com", "sender_password": "LEGADO"}, fh)
    email_config.load_email_config()
    assert "sender_password" not in email_config.email_config


def test_proxy_password_only_from_env(monkeypatch):
    monkeypatch.setenv("PROXY_PASSWORD", "px")
    assert proxy_config.get_proxy_password() == "px"
    monkeypatch.delenv("PROXY_PASSWORD", raising=False)
    assert proxy_config.get_proxy_password() == ""


def test_proxy_setter_blocked():
    try:
        proxy_config.set_proxy_password("x")
        raise AssertionError("debió lanzar RuntimeError")
    except RuntimeError as exc:
        assert "PROXY_PASSWORD" in str(exc)


def test_proxy_save_never_persists_password(isolated_fs):
    proxy_config.proxy_config = {"host": "h", "password": "LEGADO"}
    proxy_config.save_proxy_config()
    saved = json.loads(open("proxy_config.json", encoding="utf-8").read())
    assert "password" not in saved


def test_proxy_load_purges_legacy_password(isolated_fs):
    with open("proxy_config.json", "w", encoding="utf-8") as fh:
        json.dump({"host": "h", "password": "LEGADO"}, fh)
    proxy_config.load_proxy_config()
    assert "password" not in proxy_config.proxy_config


def test_email_generic_settings_crud(isolated_fs):
    email_config.load_email_config()
    email_config.set_email_setting("smtp_port", 2525)
    assert email_config.get_email_setting("smtp_port") == 2525
    assert "smtp_port" in email_config.get_all_email_settings()
    email_config.set_smtp_server("smtp.x.com")
    assert email_config.get_smtp_server() == "smtp.x.com"
    email_config.set_smtp_port(465)
    assert email_config.get_smtp_port() == 465
    email_config.disable_tls()
    assert email_config.is_tls_enabled() is False
    email_config.enable_tls()
    assert email_config.is_tls_enabled() is True
    email_config.set_sender_email("a@b.com")
    assert email_config.get_sender_email() == "a@b.com"
    email_config.reset_email_config()
    assert email_config.get_smtp_server() == "smtp.gmail.com"


def test_email_import_validate_backup_restore(isolated_fs):
    email_config.reset_email_config()
    backup = email_config.backup_email_config()
    assert backup.startswith("email_config_backup_")
    email_config.set_smtp_port(2525)
    assert email_config.restore_email_config(backup) is True
    assert email_config.restore_email_config("no-existe.json") is False
    assert email_config.validate_email_config() == []
    email_config.email_config["smtp_port"] = "mal"
    assert email_config.validate_email_config() != []
    summary = email_config.get_email_config_summary()
    assert set(summary) == {"smtp_server", "smtp_port", "use_tls"}


def test_proxy_generic_settings_crud(isolated_fs):
    proxy_config.load_proxy_config()
    proxy_config.set_proxy_setting("host", "proxy.x")
    assert proxy_config.get_proxy_setting("host") == "proxy.x"
    assert "host" in proxy_config.get_all_proxy_settings()
    proxy_config.set_proxy_host("h2")
    assert proxy_config.get_proxy_host() == "h2"
    proxy_config.set_proxy_port(3128)
    assert proxy_config.get_proxy_port() == 3128
    proxy_config.enable_proxy()
    assert proxy_config.is_proxy_enabled() is True
    proxy_config.disable_proxy()
    assert proxy_config.is_proxy_enabled() is False
    proxy_config.set_proxy_username("u")
    assert proxy_config.get_proxy_username() == "u"
    proxy_config.reset_proxy_config()
    assert proxy_config.get_proxy_host() == ""


def test_proxy_import_validate_backup(isolated_fs):
    proxy_config.reset_proxy_config()
    proxy_config.export_proxy_config("px.json")
    assert proxy_config.import_proxy_config("px.json") is True
    assert proxy_config.import_proxy_config("no-existe.json") is False
    assert proxy_config.validate_proxy_config() == []
    backup = proxy_config.backup_proxy_config()
    assert backup.startswith("proxy_config_backup_")
    assert proxy_config.restore_proxy_config(backup) is True
    summary = proxy_config.get_proxy_config_summary()
    assert "host" in summary
    proxy_config.proxy_config["port"] = "mal"
    assert proxy_config.validate_proxy_config() != []
