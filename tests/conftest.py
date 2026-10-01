"""Fixtures globales: API key ficticia y aislamiento de archivos en tmp_path."""

import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("OMDB_API_KEY", "test-key")

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def isolated_fs(tmp_path, monkeypatch):
    """Ejecuta cada test en un cwd temporal (JSON de datos aislados)."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture()
def sample_movie():
    return {
        "Title": "Matrix",
        "Year": "1999",
        "imdbRating": "8.7",
        "Genre": "Sci-Fi",
        "Director": "Wachowski",
        "Actors": "Keanu Reeves",
        "Plot": "Neo descubre la verdad",
        "Language": "English",
        "Country": "USA",
        "Awards": "4 Oscars",
        "Poster": "http://x/poster.jpg",
    }
