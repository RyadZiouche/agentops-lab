"""Télécharge les 5 réunions QMSum (domaine Produit) dans data/raw/qmsum/.

À lancer depuis la racine du dépôt :  python scripts/fetch_qmsum.py
Les données sont ignorées par git (data/raw/) : seul ce script est versionné.
"""
import json
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/Yale-LILY/QMSum/main/data/Product/all"
MEETINGS = ["IS1009d", "ES2004c", "ES2003a", "ES2015b", "IS1003b"]
DEST = Path("data/raw/qmsum")
REQUIRED_KEYS = {
    "meeting_transcripts",
    "topic_list",
    "general_query_list",
    "specific_query_list",
}


def download(meeting_id: str) -> bytes:
    """Récupère le fichier brut d'une réunion (échoue si le réseau ou l'adresse est mauvais)."""
    url = f"{BASE_URL}/{meeting_id}.json"
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def validate(raw: bytes) -> dict:
    """Vérifie que c'est du JSON valide avec les 4 blocs attendus."""
    data = json.loads(raw)
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(f"clés manquantes : {sorted(missing)}")
    return data


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    failures = []
    for meeting_id in MEETINGS:
        target = DEST / f"{meeting_id}.json"
        if target.exists():
            print(f"= {meeting_id} déjà présent, ignoré")
            continue
        try:
            raw = download(meeting_id)
            data = validate(raw)
        except Exception as error:
            print(f"! {meeting_id} échec : {error}")
            failures.append(meeting_id)
            continue
        tmp = target.with_suffix(".tmp")
        tmp.write_bytes(raw)   # écriture dans un fichier temporaire...
        tmp.rename(target)     # ...puis renommage : jamais de fichier à moitié écrit
        print(
            f"+ {meeting_id} : {len(data['meeting_transcripts'])} tours, "
            f"{len(data['specific_query_list'])} questions"
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
