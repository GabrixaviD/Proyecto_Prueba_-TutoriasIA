"""Tests de los modelos de dominio (Fase 3)."""

from models import Movie, Series


def test_movie_from_omdb_full(sample_movie):
    movie = Movie.from_omdb(sample_movie)
    assert movie.title == "Matrix"
    assert movie.year == "1999"
    assert movie.imdb_rating == "8.7"
    assert movie.director == "Wachowski"


def test_movie_from_omdb_missing_keys():
    movie = Movie.from_omdb({})
    assert movie.title == ""
    assert movie.imdb_rating == "N/A"


def test_movie_from_omdb_not_a_dict():
    movie = Movie.from_omdb(None)
    assert movie.title == ""


def test_movie_to_dict_roundtrip(sample_movie):
    movie = Movie.from_omdb(sample_movie)
    data = movie.to_dict()
    assert data["title"] == "Matrix"
    assert set(data) == {
        "title", "year", "imdb_rating", "genre", "director", "actors",
        "plot", "language", "country", "awards", "poster",
    }


def test_series_from_tvmaze_wrapped():
    raw = {"show": {"name": "Dark", "language": "German",
                    "genres": ["Drama"],
                    "rating": {"average": 8.7}, "status": "Ended"}}
    series = Series.from_tvmaze(raw)
    assert series.name == "Dark"
    assert series.genres == ["Drama"]
    assert series.rating == "8.7"
    assert series.status == "Ended"


def test_series_from_tvmaze_bare_and_missing():
    series = Series.from_tvmaze({"name": "X"})
    assert series.name == "X"
    assert series.rating == "N/A"
    assert Series.from_tvmaze({}).name == ""
    assert Series.from_tvmaze(None).name == ""


def test_series_to_dict_roundtrip():
    series = Series.from_tvmaze({"show": {"name": "Dark"}})
    data = series.to_dict()
    assert data["name"] == "Dark"
    assert isinstance(data["genres"], list)
