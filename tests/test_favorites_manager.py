"""Tests de favorites_manager (Fase 4: sin bare except)."""

import favorites_manager
from favorites_manager import (
    add_favorite,
    backup_favorites,
    clear_favorites,
    export_favorites,
    get_favorite,
    get_favorites,
    get_favorites_count,
    get_favorites_stats,
    get_favorites_summary,
    get_recent_favorites,
    import_favorites,
    load_favorites,
    remove_favorite,
    restore_favorites,
    save_favorites,
    search_favorites,
    sort_favorites,
    validate_favorites,
)


def _reset():
    favorites_manager.favorites = []


def test_add_and_count(isolated_fs, sample_movie):
    _reset()
    assert add_favorite(sample_movie) is True
    assert get_favorites_count() == 1


def test_remove_favorite(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    assert remove_favorite("Matrix") is True
    assert get_favorites_count() == 0
    assert remove_favorite("Inexistente") is False


def test_search_favorites(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    assert len(search_favorites("matr")) == 1
    assert search_favorites("zzzzz") == []


def test_sort_favorites_fallback_on_bad_data(isolated_fs):
    _reset()
    favorites_manager.favorites = ["no-es-dict", None]
    result = sort_favorites("Title")
    assert result == ["no-es-dict", None]  # sin lanzar, devuelve copia


def test_stats_skips_invalid_ratings(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    favorites_manager.favorites.append({"Title": "Mala", "imdbRating": "N/A"})
    favorites_manager.favorites.append({"Title": "Rota", "imdbRating": "xyz"})
    stats = get_favorites_stats()
    assert stats["total"] == 3
    assert stats["avg_rating"] == 8.7


def test_sort_favorites_and_fallback_key(isolated_fs, sample_movie):
    _reset()
    other = dict(sample_movie, Title="Avatar")
    add_favorite(sample_movie)
    add_favorite(other)
    ordered = sort_favorites("Title")
    assert [f["Title"] for f in ordered] == ["Avatar", "Matrix"]


def test_stats_avg_rating(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    stats = get_favorites_stats()
    assert stats["total"] == 1
    assert stats["avg_rating"] == 8.7


def test_clear_favorites(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    clear_favorites()
    assert get_favorites_count() == 0


def test_getters_and_duplicates(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    assert add_favorite(dict(sample_movie)) is False  # duplicado
    assert get_favorites_count() == 1
    assert get_favorite("Matrix")["Year"] == "1999"
    assert get_favorite("Nadie") is None
    assert len(get_favorites()) == 1


def test_save_load_export_import(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    save_favorites()
    _reset()
    load_favorites()
    assert get_favorites_count() == 1
    export_favorites("fav.json")
    _reset()
    assert import_favorites("fav.json") is True
    assert import_favorites("no-existe.json") is False
    assert get_favorites_count() == 1


def test_recent_backup_restore_validate_summary(isolated_fs, sample_movie):
    _reset()
    add_favorite(sample_movie)
    assert len(get_recent_favorites(1)) == 1
    backup = backup_favorites()
    assert backup.startswith("favorites_backup_")
    _reset()
    assert restore_favorites(backup) is True
    assert validate_favorites() == []
    favorites_manager.favorites.append({"Year": "2000"})
    assert validate_favorites() != []
    summary = get_favorites_summary()
    assert summary["total"] == 2
    assert "Sci-Fi" in summary["genres"]
