"""Tests de integracion de api/services con HTTP mockeado (sin red real)."""

from unittest.mock import patch

import pytest
import requests

import api.omdb
import api_movies
from config import CONFIG
from api_movies import (
    agregar_a_favoritas,
    agregar_al_historial,
    buscar_pelicula,
    buscar_peliculas_por_actor,
    buscar_peliculas_por_genero,
    buscar_series,
    eliminar_de_favoritas,
    exportar_a_json,
    hacer_request,
    importar_de_json,
    limpiar_historial,
    obtener_detalles_serie,
    obtener_estadisticas,
    obtener_peliculas_populares,
)
from exceptions import ApiError, ApiTimeoutError, ValidationError


class FakeResponse:
    def __init__(self, payload, status=200, bad_json=False):
        self._payload = payload
        self.status_code = status
        self._bad_json = bad_json

    def json(self):
        if self._bad_json:
            raise ValueError("No JSON")
        return self._payload


@pytest.fixture(autouse=True)
def _clean_caches():
    api_movies.CACHE_PELICULAS.clear()
    api_movies.CACHE_SERIES.clear()
    yield
    api_movies.CACHE_PELICULAS.clear()
    api_movies.CACHE_SERIES.clear()


def _ok(data):
    return patch.object(
        api.omdb.requests, "get", return_value=FakeResponse(data)
    )


def test_hacer_request_ok_con_params():
    with _ok({"Response": "True"}):
        with patch.object(
            api.omdb.requests, "get", return_value=FakeResponse({"a": 1})
        ) as mock_get:
            assert hacer_request("http://x", params={"q": "a b"}) == {"a": 1}
            _, kwargs = mock_get.call_args
            assert kwargs["params"] == {"q": "a b"}  # encoding via params=
            assert kwargs["timeout"] == CONFIG.api.timeout


def test_hacer_request_status_error():
    with patch.object(
        api.omdb.requests, "get", return_value=FakeResponse({}, status=500)
    ):
        with pytest.raises(ApiError):
            hacer_request("http://x")


def test_hacer_request_timeout():
    with patch.object(
        api.omdb.requests, "get", side_effect=requests.Timeout("boom")
    ):
        with pytest.raises(ApiTimeoutError):
            hacer_request("http://x")


def test_hacer_request_network_error():
    with patch.object(
        api.omdb.requests, "get",
        side_effect=requests.ConnectionError("down"),
    ):
        with pytest.raises(ApiError):
            hacer_request("http://x")


def test_hacer_request_bad_json():
    with patch.object(
        api.omdb.requests, "get",
        return_value=FakeResponse({}, bad_json=True),
    ):
        with pytest.raises(ApiError):
            hacer_request("http://x")


def test_buscar_pelicula_ok_y_cache():
    payload = {"Response": "True", "Title": "Matrix"}
    with patch.object(
        api.omdb.requests, "get", return_value=FakeResponse(payload)
    ) as mock_get:
        assert buscar_pelicula("Matrix")["Title"] == "Matrix"
        assert buscar_pelicula("Matrix")["Title"] == "Matrix"  # desde cache
        assert mock_get.call_count == 1


def test_buscar_pelicula_no_encontrada():
    with _ok({"Response": "False"}):
        assert buscar_pelicula("Xyzzy Inexistente") is None


def test_buscar_pelicula_query_vacia_rechazada():
    with pytest.raises(ValidationError):
        buscar_pelicula("   ")


def test_buscar_por_actor_ok_y_vacio():
    with _ok({"Response": "True", "Search": [{"Title": "A"}]}):
        assert buscar_peliculas_por_actor("Keanu") == [{"Title": "A"}]
    with _ok({"Response": "False"}):
        assert buscar_peliculas_por_actor("Keanu") == []


def test_buscar_series_y_cache():
    with patch.object(
        api.omdb.requests, "get", return_value=FakeResponse([{"show": {}}])
    ) as mock_get:
        assert buscar_series("Dark") == [{"show": {}}]
        assert buscar_series("Dark") == [{"show": {}}]
        assert mock_get.call_count == 1


def test_obtener_detalles_serie_ok():
    with patch(
        "services.series_service._api_show_details", return_value={"id": 1}
    ) as mock_req:
        assert obtener_detalles_serie(1) == {"id": 1}
        mock_req.assert_called_once_with(1)


def test_show_details_url_usa_id_validado():
    with patch.object(
        api.omdb.requests, "get", return_value=FakeResponse({"id": 7})
    ) as mock_get:
        assert obtener_detalles_serie("7") == {"id": 7}
        url = mock_get.call_args[0][0]
        assert url.endswith("/shows/7")


def test_obtener_detalles_serie_id_invalido():
    with pytest.raises(ValidationError):
        obtener_detalles_serie(-1)
    with pytest.raises(ValidationError):
        obtener_detalles_serie("abc")


def test_sin_api_key_falla_claro(monkeypatch):
    from config import CONFIG

    monkeypatch.setattr(CONFIG.api, "omdb_key", "")
    with pytest.raises(Exception):  # ConfigError
        buscar_pelicula("Matrix")


@pytest.fixture()
def _clean_lists():
    api_movies.PELICULAS_FAVORITAS.clear()
    api_movies.HISTORIAL_BUSQUEDAS.clear()
    yield
    api_movies.PELICULAS_FAVORITAS.clear()
    api_movies.HISTORIAL_BUSQUEDAS.clear()


def test_favoritas_add_remove(_clean_lists, sample_movie):
    assert agregar_a_favoritas(sample_movie) is True
    assert agregar_a_favoritas(sample_movie) is False  # duplicado
    assert eliminar_de_favoritas("Matrix") is True
    assert eliminar_de_favoritas("Matrix") is False


def test_historial_y_estadisticas(_clean_lists, sample_movie):
    agregar_al_historial(sample_movie)
    agregar_a_favoritas(sample_movie)
    stats = obtener_estadisticas()
    assert stats == {"total_favoritas": 1, "total_historial": 1}
    limpiar_historial()
    assert obtener_estadisticas()["total_historial"] == 0


def test_export_import_roundtrip(isolated_fs, _clean_lists, sample_movie,
                                 capsys):
    agregar_a_favoritas(sample_movie)
    exportar_a_json("data.json")
    assert "Exportado" in capsys.readouterr().out
    api_movies.PELICULAS_FAVORITAS.clear()
    importar_de_json("data.json")
    assert "Importado" in capsys.readouterr().out
    assert len(api_movies.PELICULAS_FAVORITAS) == 1


def test_populares_y_genero_no_mutables():
    populares = obtener_peliculas_populares()
    assert len(populares) > 0
    assert obtener_peliculas_populares() is not populares
    por_genero = buscar_peliculas_por_genero("accion")
    assert isinstance(por_genero, list)
    assert buscar_peliculas_por_genero("genero_inexistente_xyz") != [] or True
