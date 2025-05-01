from __future__ import annotations
"""ppt_builder.py (Python 3.9‑compatible)
--------------------------------------------------
Fills the cleaned PowerPoint template with narrative, ratings, and images.
All shapes are addressed **by name** (set once in the template’s Selection
Pane).  If a shape is missing the builder skips it rather than crashing.
"""

from pathlib import Path
from typing import Dict, List, Union, Optional

from pptx import Presentation
from pptx.util import Inches

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _set_text(shape, new_text: str) -> None:
    """Safely replace the text in a shape if it exists."""
    if shape is None or not shape.has_text_frame:
        return
    shape.text = new_text


def _safe_shape(slide, target: str):
    """Return the first shape whose .name matches *target* (case-sensitive)."""
    for shp in slide.shapes:
        if shp.name == target:
            return shp
    return None


def _resize_bar(shape, score: float, max_score: float, max_width_emu: int) -> None:
    """Resize a rectangle horizontally according to *score* (left edge fixed)."""
    if shape is None or shape.has_text_frame:
        return
    shape.width = int(max_width_emu * (score / max_score))


def _reposition_ball(ball, rating: int, track_left_emu: int, track_right_emu: int) -> None:
    """Move the ball along a horizontal track based on a 1‒5 rating."""
    if ball is None:
        return
    frac = (rating - 1) / 4  # 0.0 → 1.0
    ball.left = track_left_emu + int((track_right_emu - track_left_emu) * frac)


# ---------------------------------------------------------------------------
# Main public helper
# ---------------------------------------------------------------------------

def build_report_pptx(
    template_path: Union[str, Path],
    output_path: Union[str, Path],
    *,
    candidate_name: str,
    role_and_company: str,
    personal_profile: str,
    strengths: List[Dict[str, str]],
    development_areas: List[Dict[str, str]],
    future_considerations: str,
    personal_development: List[Dict[str, str]],
    org_support: List[Dict[str, str]],
    radar_chart_1_path: Optional[Union[str, Path]] = None,
    radar_chart_2_path: Optional[Union[str, Path]] = None,
    bar_scores: Optional[Dict[str, float]] = None,
    summary_ratings: Optional[Dict[str, int]] = None,
    reasoning_scores: Optional[Dict[str, int]] = None,
) -> Path:
    """Fill the PowerPoint template and save it.

    Parameters
    ----------
    template_path, output_path
        Either *str* or *pathlib.Path* – will be converted to `str` for python‑pptx.

    Returns
    -------
    Path
        The path to the saved file (useful for Streamlit’s download button).
    """

    prs = Presentation(str(template_path))

    # ------------------------------------------------------------------
    # Slide 1 – basics
    # ------------------------------------------------------------------
    s1 = prs.slides[0]
    _set_text(_safe_shape(s1, "candidate_name"), candidate_name)
    _set_text(_safe_shape(s1, "role_company"), role_and_company)

    # ------------------------------------------------------------------
    # Slide 3 – narrative & green balls
    # ------------------------------------------------------------------
    s3 = prs.slides[2]
    _set_text(_safe_shape(s3, "personal_profile"), personal_profile)

    for i in range(3):
        _set_text(_safe_shape(s3, f"strength_{i+1}_title"), strengths[i]["title"])
        _set_text(_safe_shape(s3, f"strength_{i+1}_body"), strengths[i]["paragraph"])
        _set_text(_safe_shape(s3, f"dev_{i+1}_title"), development_areas[i]["title"])
        _set_text(_safe_shape(s3, f"dev_{i+1}_body"), development_areas[i]["paragraph"])

    _set_text(_safe_shape(s3, "future_considerations"), future_considerations)

    if summary_ratings:
        track_left = Inches(1.2).emu
        track_right = Inches(6.5).emu
        _reposition_ball(_safe_shape(s3, "ball_fit"), summary_ratings.get("Fit for Role", 3), track_left, track_right)
        _reposition_ball(_safe_shape(s3, "ball_cap"), summary_ratings.get("Capabilities", 3), track_left, track_right)
        _reposition_ball(_safe_shape(s3, "ball_pot"), summary_ratings.get("Potential", 3), track_left, track_right)
        _reposition_ball(_safe_shape(s3, "ball_future"), summary_ratings.get("Future Considerations", 3), track_left, track_right)

    # ------------------------------------------------------------------
    # Slide 4 – development suggestions
    # ------------------------------------------------------------------
    s4 = prs.slides[3]
    for i in range(2):
        _set_text(_safe_shape(s4, f"pd_{i+1}_title"), personal_development[i]["title"])
        _set_text(_safe_shape(s4, f"pd_{i+1}_body"), personal_development[i]["paragraph"])
        _set_text(_safe_shape(s4, f"org_{i+1}_title"), org_support[i]["title"])
        _set_text(_safe_shape(s4, f"org_{i+1}_body"), org_support[i]["paragraph"])

    # ------------------------------------------------------------------
    # Slide 5 – eight energy bars
    # ------------------------------------------------------------------
    if bar_scores:
        s5 = prs.slides[4]
        max_width = Inches(5.5).emu
        name_map = {
            "purpose energy": "bar_purpose",
            "intellectual energy": "bar_intellectual",
            "emotional energy": "bar_emotional",
            "people energy": "bar_people",
            "performance impact": "bar_performance",
            "strategic framing": "bar_strategic",
            "mobilisation": "bar_mobilisation",
            "powerful relationships": "bar_relationships",
        }
        for label, score in bar_scores.items():
            shape_name = name_map.get(label.lower())
            if shape_name:
                _resize_bar(_safe_shape(s5, shape_name), score, 5.0, max_width)

    # ------------------------------------------------------------------
    # Slide 6 – radar charts
    # ------------------------------------------------------------------
    s6 = prs.slides[5]
    if radar_chart_1_path and Path(radar_chart_1_path).exists():
        ph1 = _safe_shape(s6, "spider_1")
        if ph1:
            s6.shapes.add_picture(str(radar_chart_1_path), ph1.left, ph1.top, ph1.width, ph1.height)
            ph1._element.getparent().remove(ph1._element)

    if radar_chart_2_path and Path(radar_chart_2_path).exists():
        ph2 = _safe_shape(s6, "spider_2")
        if ph2:
            s6.shapes.add_picture(str(radar_chart_2_path), ph2.left, ph2.top, ph2.width, ph2.height)
            ph2._element.getparent().remove(ph2._element)

    # ------------------------------------------------------------------
    # Slide 7 – reasoning bars
    # ------------------------------------------------------------------
    if reasoning_scores:
        s7 = prs.slides[6]
        max_width = Inches(5.5).emu
        for label, score in reasoning_scores.items():
            lname = label.lower()
            _resize_bar(_safe_shape(s7, f"bar_{lname}"), float(score), 100.0, max_width)
            _set_text(_safe_shape(s7, f"label_{lname}"), f"{score}%")

    # ------------------------------------------------------------------
    # Save and return path
    # ------------------------------------------------------------------
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    return out_path
