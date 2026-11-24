import json
from pathlib import Path

from app.segment import Segment


def load_qmsum(path: Path) -> list[Segment]:
    """Lit un fichier QMSum et renvoie un Segment par tour de parole."""
    with open(path, encoding="utf-8") as f:
        meeting = json.load(f)

    source_id = path.stem  # "ES2003a"
    return [
        Segment(
            texte=tour["content"],
            source_id=source_id,
            position=i,  # base 0, comme relevant_text_span
            locuteur=tour["speaker"],
        )
        for i, tour in enumerate(meeting["meeting_transcripts"])
    ]