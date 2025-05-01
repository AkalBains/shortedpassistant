"""trait_scores.py – helper utilities for score aggregation (Python 3.9)
---------------------------------------------------------------------
Converts the consultant’s 24 granular trait ratings (1‑5 integers or the
corresponding strings) into bar‑chart and radar‑chart structures.
"""

from statistics import mean
from typing import Dict, Tuple, Union

# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

_SCALE_MAP = {
    "below": 1,
    "developing": 2,
    "hits": 3,
    "good": 4,
    "strong": 5,
}


def _to_numeric(val: Union[int, float, str]) -> int:
    """Convert a rating to an integer 1‑5.

    Accepts numeric 1‑5 or the label strings (Below, Developing, …).
    Raises *ValueError* for anything else.
    """
    if isinstance(val, (int, float)):
        iv = int(val)
        if 1 <= iv <= 5:
            return iv
    elif isinstance(val, str):
        key = val.strip().lower()
        if key in _SCALE_MAP:  # pragma: no branch
            return _SCALE_MAP[key]
    raise ValueError(f"Unsupported rating value: {val!r}")


# ---------------------------------------------------------------------------
# Trait → group mappings
# ---------------------------------------------------------------------------

_GROUP_MAP = {
    "purpose energy": ["mission", "drive", "agency"],
    "intellectual energy": ["judgment", "incisiveness", "curiosity"],
    "emotional energy": ["positivity", "resilience", "growth mindset"],
    "people energy": ["compelling impact", "connection", "environmental insight"],

    "performance impact": [
        "achieves sustainable impact",
        "creates focus",
        "orchestrates delivery",
    ],
    "strategic framing": [
        "frames complexity",
        "identifies new possibilities",
        "generates solutions",
    ],
    "mobilisation": ["inspires people", "drives culture", "grows self and others"],
    "powerful relationships": ["aligns stakeholders", "models collaboration", "builds teams"],
}

_RADAR1_TRAITS = [
    "mission", "drive", "agency",
    "incisiveness", "curiosity",
    "positivity", "resilience", "growth mindset",
    "compelling impact", "connection", "environmental insight",
]
_RADAR2_TRAITS = [
    "achieves sustainable impact", "creates focus", "orchestrates delivery",
    "frames complexity", "identifies new possibilities", "generates solutions",
    "inspires people", "drives culture", "grows self and others",
    "aligns stakeholders", "models collaboration", "builds teams",
]

# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def aggregate_eight_scores(detailed_ratings: Dict[str, Union[int, str]]) -> Dict[str, float]:
    """Return the 8 energy‑bar scores (floats rounded to 2 d.p.)."""
    norm = {k.lower(): _to_numeric(v) for k, v in detailed_ratings.items()}
    scores: Dict[str, float] = {}

    for group, traits in _GROUP_MAP.items():
        try:
            values = [norm[t] for t in traits]
        except KeyError as missing:
            raise ValueError(f"Missing rating for trait: {missing.args[0]}") from None
        scores[group] = round(mean(values), 2)

    return scores


def split_radar_groups(detailed_ratings: Dict[str, Union[int, str]]) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Return two dicts for radar‑chart #1 and #2 (numeric 1‑5)."""
    norm = {k.lower(): _to_numeric(v) for k, v in detailed_ratings.items()}
    radar1 = {trait: norm[trait] for trait in _RADAR1_TRAITS}
    radar2 = {trait: norm[trait] for trait in _RADAR2_TRAITS}
    return radar1, radar2

