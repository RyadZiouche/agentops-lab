from dataclasses import dataclass

@dataclass(frozen=True)
class Segment:
    # Champs obligatoires
    texte: str
    source_id: str
    position: int
    # Champs optionnels
    locuteur: str | None = None
    debut: float | None = None  # secondes depuis le début de la réunion
    fin: float | None = None