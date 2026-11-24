from pathlib import Path

import pytest

from app.loaders.qmsum import load_qmsum

FICHIER = Path("data/raw/qmsum/ES2003a.json")

pytestmark = pytest.mark.skipif(
    not FICHIER.exists(), reason="données QMSum absentes (data/raw/ est ignoré par git)"
)


def test_nombre_de_segments():
    segs = load_qmsum(FICHIER)
    assert len(segs) == 122


def test_segment_56():
    seg = load_qmsum(FICHIER)[56]
    assert seg.source_id == "ES2003a"
    assert seg.locuteur == "Project Manager"
    assert seg.texte.startswith("Cheers")


def test_positions_continues():
    positions = [s.position for s in load_qmsum(FICHIER)]
    assert positions == list(range(122))
    