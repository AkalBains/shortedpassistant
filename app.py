from __future__ import annotations
"""app.py – single‑page Streamlit app (Python 3.9)
------------------------------------------------
The *first* Streamlit command executed **must** be `st.set_page_config`, so we
import Streamlit, set the page config, and *then* import everything else.
"""

import streamlit as st

# Page‑level configuration must come before any other st.* call or decorator.
st.set_page_config(page_title="Leadership Report Generator", layout="wide")

# ---------------------------------------------------------------------------
# Standard & local imports (safe after set_page_config)
# ---------------------------------------------------------------------------
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

from openai_api import generate_report
from trait_scores import aggregate_eight_scores
from radar_charts import build_radar_charts
from ppt_builder import build_report_pptx

# ---------------------------------------------------------------------------
# Configuration & caching
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
TEMPLATE_PATH = ROOT / "templates" / "Executive_Report_template_v2.pptx"

@st.cache_resource(show_spinner=False)
def _load_template_bytes() -> bytes:  # noqa: D401 – keep short description
    """Cache PPTX bytes so repeated runs don’t hit disk."""
    return TEMPLATE_PATH.read_bytes()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TRAIT_24 = [
    "mission", "drive", "agency",
    "judgment", "incisiveness", "curiosity",
    "positivity", "resilience", "growth mindset",
    "compelling impact", "connection", "environmental insight",
    "achieves sustainable impact", "creates focus", "orchestrates delivery",
    "frames complexity", "identifies new possibilities", "generates solutions",
    "inspires people", "drives culture", "grows self and others",
    "aligns stakeholders", "models collaboration", "builds teams",
]

# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

def main() -> None:  # noqa: C901 – Streamlit code can be long
    st.title("📝 Leadership Report Generator")
    st.write(
        "Fill in the form, click *Generate Report*, and download a fully‑formatted PowerPoint.")

    # --------------------  INPUT FORM  --------------------
    with st.form("report_form", clear_on_submit=False):
        st.header("Candidate Basics")
        candidate_name = st.text_input("Candidate Name", max_chars=80)
        role_and_company = st.text_input("Role & Company", max_chars=120)

        st.header("Consultant's Raw Notes")
        raw_notes = st.text_area("Paste or type your assessment notes here", height=200)

        st.header("Quadrant Ratings (1 = Developing → 5 = Strong)")
        cols1 = st.columns(4)
        fit_for_role = cols1[0].slider("Fit for Role", 1, 5, 3)
        capabilities = cols1[1].slider("Capabilities", 1, 5, 3)
        potential = cols1[2].slider("Potential", 1, 5, 3)
        future_consider = cols1[3].slider("Future Considerations", 1, 5, 3)

        st.header("24 Trait Ratings (1 = Developing → 5 = Strong)")
        detailed_ratings: Dict[str, int] = {}
        for i in range(0, 24, 4):
            cols = st.columns(4)
            for j, trait in enumerate(TRAIT_24[i : i + 4]):
                key = f"trait_{trait.replace(' ', '_')}"
                detailed_ratings[trait] = cols[j].slider(trait.title(), 1, 5, 3, key=key)

        st.header("Reasoning Scores (percentile 1–99)")
        cols2 = st.columns(4)
        reasoning_scores = {
            "verbal": cols2[0].number_input("Verbal", 1, 99, 50, key="verbal"),
            "numerical": cols2[1].number_input("Numerical", 1, 99, 50, key="numerical"),
            "abstract": cols2[2].number_input("Abstract", 1, 99, 50, key="abstract"),
            "overall": cols2[3].number_input("Overall", 1, 99, 50, key="overall"),
        }

        submitted = st.form_submit_button("🚀 Generate Report")

    if not submitted:
        st.stop()

    # --------------------  VALIDATION  --------------------
    if not candidate_name or not role_and_company or not raw_notes.strip():
        st.error("Please fill in Candidate Name, Role & Company, and Raw Notes before generating the report.")
        st.stop()

    # --------------------  GPT CALL  --------------------
    with st.spinner("Talking to GPT…"):
        try:
            gpt_json = generate_report(raw_notes)
            expanded = json.loads(gpt_json)
        except Exception as exc:  # noqa: BLE001
            st.exception(exc)
            st.stop()

    # --------------------  SCORE AGGREGATION & CHARTS  --------------------
    overall_ratings = {
        "Fit for Role": fit_for_role,
        "Capabilities": capabilities,
        "Potential": potential,
        "Future Considerations": future_consider,
    }

    bar_scores = aggregate_eight_scores(detailed_ratings)

    with TemporaryDirectory() as tmpdir, st.spinner("Drawing radar charts…"):
        radar1_path, radar2_path = build_radar_charts(detailed_ratings, Path(tmpdir))

        # --------------------  BUILD POWERPOINT  --------------------
        output_path = Path(tmpdir) / f"Executive_Report_{candidate_name.replace(' ', '_')}.pptx"
        with st.spinner("Building PowerPoint…"):
            build_report_pptx(
                template_path=TEMPLATE_PATH,
                output_path=output_path,
                candidate_name=candidate_name,
                role_and_company=role_and_company,
                personal_profile=expanded["personal_profile"],
                strengths=expanded["strengths"],
                development_areas=expanded["development_areas"],
                future_considerations=expanded["future_considerations"],
                personal_development=expanded["personal_development"],
                org_support=expanded["org_support"],
                radar_chart_1_path=radar1_path,
                radar_chart_2_path=radar2_path,
                bar_scores=bar_scores,
                summary_ratings=overall_ratings,
                reasoning_scores=reasoning_scores,
            )

        # --------------------  DOWNLOAD LINK  --------------------
        st.success("Done! Click below to download your report.")
        with open(output_path, "rb") as ppt_file:
            st.download_button(
                label="⬇️ Download PowerPoint",
                data=ppt_file.read(),
                file_name=output_path.name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )


if __name__ == "__main__":
    main()

