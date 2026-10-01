"""Tests unitarios de utils: validacion (Fase 5) y formato (Fase 4)."""

import pytest

import utils
from exceptions import ValidationError


def test_validate_email_ok():
    assert utils.validate_email("user@example.com") is True


@pytest.mark.parametrize("bad", ["no-es-mail", "a@b", "@x.com", "", None, 123])
def test_validate_email_rejects(bad):
    assert utils.validate_email(bad) is False


def test_validate_date_ok():
    assert utils.validate_date("2024-01-31") is True


@pytest.mark.parametrize("bad", ["31/01/2024", "no-fecha", "", None, "2024-13-01"])
def test_validate_date_rejects(bad):
    assert utils.validate_date(bad) is False


def test_validate_search_query_ok_strips():
    assert utils.validate_search_query("  Matrix  ") == "Matrix"


@pytest.mark.parametrize("bad", ["", "   ", "a" * 201, "a; DROP TABLE x", None])
def test_validate_search_query_rejects(bad):
    with pytest.raises(ValidationError):
        utils.validate_search_query(bad)


def test_validate_positive_int_ok():
    assert utils.validate_positive_int("42", "id") == 42
    assert utils.validate_positive_int(7, "id") == 7


@pytest.mark.parametrize("bad", ["0", "-5", "abc", "", None, 3.9])
def test_validate_positive_int_rejects(bad):
    with pytest.raises(ValidationError):
        utils.validate_positive_int(bad, "id")


def test_format_movie_display_full(sample_movie):
    out = utils.format_movie_display(sample_movie)
    assert "Matrix" in out and "1999" in out and "Wachowski" in out


def test_format_movie_display_missing_keys_uses_na(sample_movie):
    del sample_movie["Director"]
    assert "Director: N/A" in utils.format_movie_display(sample_movie)


def test_format_movie_display_none():
    assert "No se encontr" in utils.format_movie_display(None)


def test_sort_items_ok_and_fallback():
    items = [{"n": "b"}, {"n": "a"}]
    assert [i["n"] for i in utils.sort_items(items, "n")] == ["a", "b"]
    # Elementos no-ordenables -> devuelve la lista original sin lanzar
    assert utils.sort_items([1, "a", None], "n") == [1, "a", None]


def test_remove_duplicates_and_filter():
    assert utils.remove_duplicates([1, 1, 2]) == [1, 2]
    items = [{"g": "x"}, {"g": "y"}]
    assert utils.filter_items(items, "g", "x") == [{"g": "x"}]


def test_format_series_display(sample_movie):
    out = utils.format_series_display({"show": {"name": "Dark"}})
    assert "Dark" in out
    long_summary = {"show": {"name": "X", "summary": "s" * 300}}
    assert "..." in utils.format_series_display(long_summary)


def test_display_helpers_print(capsys):
    utils.print_separator()
    utils.print_header("titulo")
    utils.print_subheader("sub")
    out = capsys.readouterr().out
    assert "TITULO" in out and "sub" in out


def test_get_user_input_int(monkeypatch, capsys):
    inputs = iter(["no-numero", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert utils.get_user_input("n:", int) == 42
    assert "inválida" in capsys.readouterr().out


def test_get_user_input_str_and_float(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "hola")
    assert utils.get_user_input("t:") == "hola"
    monkeypatch.setattr("builtins.input", lambda _: "3.5")
    assert utils.get_user_input("f:", float) == 3.5


def test_delay_and_clear_screen(monkeypatch):
    calls = []
    monkeypatch.setattr(utils.time, "sleep", lambda s: calls.append(s))
    monkeypatch.setattr(utils.os, "system", lambda c: calls.append(c))
    utils.delay(1)
    utils.clear_screen()
    assert calls == [1, calls[1]]


def test_timestamp_format_date_truncate():
    assert utils.get_timestamp()[:4].isdigit()
    from datetime import datetime
    assert utils.format_date(datetime(2024, 1, 2, 3, 4, 5)) == "2024-01-02 03:04:05"
    assert utils.format_date("x") == "x"
    assert utils.truncate_text("a" * 150).endswith("...")
    assert utils.truncate_text("corto") == "corto"


def test_init_dirs_creates(isolated_fs):
    import shutil
    shutil.rmtree("results", ignore_errors=True)
    shutil.rmtree("exports", ignore_errors=True)
    utils.init_dirs()
    import os
    assert os.path.isdir("results") and os.path.isdir("exports")


def test_format_list_display_branches():
    assert "No se encontraron" in utils.format_list_display([], "serie")
    items = [{"titulo": "T", "anio": "2000"}, {"Title": "M", "Year": "1999"},
             {"name": "N"}, {"otro": 1}]
    out = utils.format_list_display(items)
    assert "1. T (2000)" in out and "M (1999)" in out
    assert "N" in out and "desconocido" in out


def test_save_and_export_helpers(isolated_fs):
    utils.init_dirs()
    path = utils.save_results([{"a": 1}], "r.txt")
    assert open(path, encoding="utf-8").read().strip() == "{'a': 1}"
    path = utils.save_results("texto", "r2.txt")
    assert open(path, encoding="utf-8").read() == "texto"
    import json
    path = utils.export_to_json([{"a": 1}], "d.json")
    assert json.loads(open(path, encoding="utf-8").read()) == [{"a": 1}]
    path = utils.export_to_csv([{"a": 1, "b": 2}], "d.csv")
    content = open(path, encoding="utf-8").read()
    assert "a,b" in content.replace("\r", "")
    assert utils.export_to_csv([], "vacio.csv").endswith("vacio.csv")


def test_menu_and_random_id(capsys):
    utils.create_menu(["Uno", "Dos"])
    out = capsys.readouterr().out
    assert "1. Uno" in out and "0. Salir" in out
    calls = []
    assert utils.handle_menu_choice("a", {"a": lambda: calls.append(1)}) is True
    assert calls == [1]
    assert utils.handle_menu_choice(0, {}) is False
    assert utils.handle_menu_choice("z", {}) is True
    assert "inválida" in capsys.readouterr().out
    assert len(utils.generate_random_id()) > 0
