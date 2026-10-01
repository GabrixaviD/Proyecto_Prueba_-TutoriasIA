"""Tests de las custom exceptions (Fase 4)."""

import pytest

from exceptions import (
    ApiError,
    ApiTimeoutError,
    AppError,
    ConfigError,
    MovieNotFoundError,
    SeriesNotFoundError,
    ValidationError,
)


def test_base_error_carries_code_and_message():
    err = AppError("algo fallo", code="APP-0001")
    assert str(err) == "algo fallo"
    assert err.code == "APP-0001"


def test_movie_not_found_carries_title_and_code():
    err = MovieNotFoundError("Matrix")
    assert isinstance(err, AppError)
    assert err.code == "MOV-4041"
    assert err.title == "Matrix"


def test_series_not_found_code():
    assert SeriesNotFoundError("Dark").code == "SER-4041"


def test_api_timeout_includes_service():
    err = ApiTimeoutError("OMDB", 30)
    assert isinstance(err, ApiError)
    assert "OMDB" in str(err)


def test_api_error_carries_status():
    assert ApiError("x", status=500).status == 500


def test_validation_error_carries_field():
    err = ValidationError("titulo", "no puede estar vacio")
    assert err.field == "titulo"
    assert err.code == "VAL-4002"


def test_config_error_code():
    assert ConfigError("falta key").code == "CFG-4001"


def test_errors_are_catchable_as_apperror():
    with pytest.raises(AppError):
        raise MovieNotFoundError("X")
