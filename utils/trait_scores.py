from __future__ import annotations
"""trait_scores.py – helper utilities for score aggregation
-----------------------------------------------------------
Converts the consultant’s 24 granular trait ratings (1‒5 integers or the
corresponding strings) into:

* **Eight bar-chart scores** for slide 5 – `aggregate_eight_scores()`
* **Two per‑trait dictionaries** for the radar‐chart generator –
  `split_radar_groups()` (optional convenience).

The mapping of traits → energy bars follows the brief:

    purpose energy        = mean(mission, drive, agency)
    intellectual energy   = mean(judgment, incisiveness, curiosity)
    emotional energy      = mean(positivity, resilience, growth mindset)
    people energy         = mean(compelling impact, connection, environmental insight)

    performance impact    = mean(achieves sustainable impact, creates focus, orchestrates delivery)
    strategic framing     = mean(frames complexity, identifies new possibilities, generates solutions)
    mobilisation          = mean(inspires people, drives culture, grows self and others)
    powerful relationships= mean(aligns stakeholders, models collaboration, builds teams)

The case of keys in `detailed_ratings` is ignored (they are normalised to
lower‑case for look‑ups).
"""

from __future__ import annotations

from statistics import mean
from typing import Dict, Tuple

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


def _to_numeric(val) -> int:
    """Accept int 1‑5 or string label and return an int 1‑5.

    Raises ValueError for anything else.
    """
    if isinstance(val, (int, float)):
        iv = int(val)
        if 1 <= iv <= 5:
            return iv
    if isinstance(val, str):
        key = val.strip().lower()
        if key in _SCALE_MAP:
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

# Two radar‑chart buckets – first 11 traits, second 13 traits
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

def aggregate_eight_scores(detailed_ratings: Dict[str, int | str]) -> Dict[str, float]:
    """Return the 8 bar‑chart scores (1‑5 floats) given 24 granular ratings.

    Missing traits are ignored, but if *all* in a group are missing a
    `ValueError` is raised so the caller can react.
    """

    # normalise keys to lower‑case
    norm = {k.lower(): _to_numeric(v) for k, v in detailed_ratings.items()}
    scores: Dict[str, float] = {}

    for group, traits in _GROUP_MAP.items():
        try:
            values = [norm[t] for t in traits]
        except KeyError as missing:
            raise ValueError(f"Missing rating for trait: {missing.args[0]}") from None
        scores[group] = round(mean(values), 2)

    return scores


def split_radar_groups(detailed_ratings: Dict[str, int | str]) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Return two dicts – personal characteristics and leadership capabilities.

    The first dict contains the 11 traits for radar‑chart #1; the second,
    the 13 traits for radar‑chart #2.  All ratings are numeric 1‒5.
    """
    norm = {k.lower(): _to_numeric(v) for k, v in detailed_ratings.items()}

    radar1 = {trait: norm[trait] for trait in _RADAR1_TRAITS}
    radar2 = {trait: norm[trait] for trait in _RADAR2_TRAITS}
    return radar1, radar2
