"""Tests de user_manager (Fase 5): hash, auth y migracion de legados."""

import json

import user_manager
from user_manager import (
    authenticate_user,
    backup_users,
    create_user,
    delete_user,
    export_users,
    get_all_users,
    get_current_user,
    get_user,
    get_user_preferences,
    get_user_stats,
    get_users_count,
    import_users,
    load_users,
    logout_user,
    restore_users,
    search_users,
    update_user,
    update_user_preferences,
    validate_user,
    validate_users_integrity,
)


def _reset():
    user_manager.users = []
    user_manager.current_user = None


def test_create_user_hashes_password(isolated_fs):
    _reset()
    ok, _ = create_user("ana", "secreto123", "ana@x.com")
    assert ok is True
    stored = user_manager.users[0]["password"]
    assert stored != "secreto123"
    assert "$" in stored  # formato salt$hash


def test_authenticate_ok_and_updates_login(isolated_fs):
    _reset()
    create_user("ana", "secreto123")
    ok, user = authenticate_user("ana", "secreto123")
    assert ok is True
    assert user["last_login"] is not None


def test_authenticate_wrong_password(isolated_fs):
    _reset()
    create_user("ana", "secreto123")
    ok, msg = authenticate_user("ana", "otra")
    assert ok is False
    assert msg == "Credenciales inválidas"


def test_duplicate_user_rejected(isolated_fs):
    _reset()
    create_user("ana", "x123456")
    ok, msg = create_user("ana", "y123456")
    assert ok is False
    assert "existe" in msg


def test_legacy_plaintext_migrates_on_login(isolated_fs):
    _reset()
    with open("users.json", "w", encoding="utf-8") as fh:
        json.dump([{"username": "viejo", "password": "plano123",
                    "last_login": None}], fh)
    load_users()
    ok, _ = authenticate_user("viejo", "plano123")
    assert ok is True
    assert "$" in user_manager.users[0]["password"]  # ya migrado a hash


def test_legacy_wrong_password_stays_plaintext(isolated_fs):
    _reset()
    with open("users.json", "w", encoding="utf-8") as fh:
        json.dump([{"username": "viejo", "password": "plano123",
                    "last_login": None}], fh)
    load_users()
    ok, _ = authenticate_user("viejo", "incorrecta")
    assert ok is False
    assert user_manager.users[0]["password"] == "plano123"


def test_crud_and_queries(isolated_fs):
    _reset()
    create_user("ana", "secreto123")
    create_user("beto", "clave4567")
    assert get_users_count() == 2
    assert get_user("ana")["username"] == "ana"
    assert get_user("nadie") is None
    assert len(search_users("an")) == 1
    assert len(get_all_users()) == 2
    assert update_user("ana", {"email": "a@b.com"}) is True
    assert update_user("nadie", {}) is False
    assert get_user("ana")["email"] == "a@b.com"
    authenticate_user("ana", "secreto123")
    assert get_current_user()["username"] == "ana"
    logout_user()
    assert get_current_user() is None
    assert delete_user("beto") is True
    assert delete_user("beto") is False


def test_preferences_and_stats(isolated_fs):
    _reset()
    create_user("ana", "secreto123")
    assert update_user_preferences("ana", {"theme": "light"}) is True
    assert update_user_preferences("nadie", {}) is False
    assert get_user_preferences("ana")["theme"] == "light"
    assert get_user_preferences("nadie") == {}
    stats = get_user_stats()
    assert stats == {"total": 1, "active": 0, "inactive": 1}
    authenticate_user("ana", "secreto123")
    assert get_user_stats()["active"] == 1


def test_export_import_backup_restore(isolated_fs):
    _reset()
    create_user("ana", "secreto123")
    export_users("exp.json")
    _reset()
    assert import_users("exp.json") is True
    assert get_users_count() == 1
    assert import_users("no-existe.json") is False
    backup = backup_users()
    assert backup.startswith("users_backup_")
    _reset()
    assert restore_users(backup) is True
    assert get_users_count() == 1


def test_validate_user_and_integrity(isolated_fs):
    _reset()
    assert validate_user("an", "123") != []  # ambos invalidos
    assert validate_user("ana", "secreto123") == []
    create_user("ana", "secreto123")
    assert validate_users_integrity() == []
    user_manager.users.append({"username": "roto"})
    errors = validate_users_integrity()
    assert any("password" in e for e in errors)
    user_manager.users.append({"password": "x"})
    assert any("username" in e for e in validate_users_integrity())
