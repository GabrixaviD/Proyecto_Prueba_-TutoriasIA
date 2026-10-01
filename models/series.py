"""Modelo de dominio: serie (Fase 3)."""

from dataclasses import asdict, dataclass, field


@dataclass
class Series:
    """Serie normalizada, independiente de la fuente (TVMaze, cache, JSON)."""

    name: str = ""
    language: str = ""
    genres: list = field(default_factory=list)
    rating: str = "N/A"
    status: str = ""
    premiered: str = ""
    ended: str = ""
    runtime: str = ""
    summary: str = ""

    @classmethod
    def from_tvmaze(cls, data: dict) -> "Series":
        """Construye desde el nodo `show` crudo de TVMaze (claves tolerantes)."""

        show = data.get("show", data) if isinstance(data, dict) else {}
        get = show.get if isinstance(show, dict) else (lambda _k, d="": d)
        rating = get("rating", {}) or {}
        return cls(
            name=str(get("name", "")),
            language=str(get("language", "")),
            genres=list(get("genres", []) or []),
            rating=str((rating or {}).get("average", "N/A")),
            status=str(get("status", "")),
            premiered=str(get("premiered", "")),
            ended=str(get("ended", "")),
            runtime=str(get("runtime", "")),
            summary=str(get("summary", "")),
        )

    def to_dict(self) -> dict:
        """Serializa a dict plano (persistencia / API)."""

        return asdict(self)


__all__ = ["Series"]
