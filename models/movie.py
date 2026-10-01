"""Modelo de dominio: pelicula (Fase 3)."""

from dataclasses import asdict, dataclass


@dataclass
class Movie:
    """Pelicula normalizada, independiente de la fuente (OMDB, cache, JSON)."""

    title: str = ""
    year: str = ""
    imdb_rating: str = "N/A"
    genre: str = ""
    director: str = ""
    actors: str = ""
    plot: str = ""
    language: str = ""
    country: str = ""
    awards: str = ""
    poster: str = ""

    @classmethod
    def from_omdb(cls, data: dict) -> "Movie":
        """Construye desde la respuesta cruda de OMDB (claves tolerantes)."""

        get = data.get if isinstance(data, dict) else (lambda _k, d="": d)
        return cls(
            title=str(get("Title", "")),
            year=str(get("Year", "")),
            imdb_rating=str(get("imdbRating", "N/A")),
            genre=str(get("Genre", "")),
            director=str(get("Director", "")),
            actors=str(get("Actors", "")),
            plot=str(get("Plot", "")),
            language=str(get("Language", "")),
            country=str(get("Country", "")),
            awards=str(get("Awards", "")),
            poster=str(get("Poster", "")),
        )

    def to_dict(self) -> dict:
        """Serializa a dict plano (persistencia / API)."""

        return asdict(self)


__all__ = ["Movie"]
