import streamlit as st
from utils.openai_api import generate_report
from utils.ppt_builder import build_report_pptx
import tempfile

# --- Streamlit config and authentication ---
st.set_page_config(page_title="Leadership Report Generator", layout="centered")
PASSWORD = st.secrets.get("APP_PASSWORD", "changeme")

def check_password():
    st.title("🔐 Leadership Report Generator Login")
    password = st.text_input("Enter the password:", type="password")
    if password == PASSWORD:
        return True
    elif password:
        st.error("Incorrect password. Please try again.")
        return False
    return False

if not check_password():
    st.stop()

# --- Page content ---
st.title(":brain: Leadership Consulting Report Generator")
st.markdown("Fill in the candidate's details, consultant notes, and ratings below.")

# === Candidate Info ===
st.header("1. Candidate Information")
candidate_name = st.text_input("Candidate Name")
role_and_company = st.text_input("Role and Company")

# === Consultant Notes ===
st.header("2. Consultant Notes")
notes = st.text_area("Paste consultant notes here (profile, strengths, development, future considerations):", height=300)

# === Ratings Dropdowns ===
st.header("3. Ratings")
rating_scale = ["Below", "Developing", "Hits", "Good", "Strong"]
rating_map = {"Below": 1, "Developing": 2, "Hits": 3, "Good": 4, "Strong": 5}

st.subheader("A. Personal Characteristics")
personal_traits = [
    "Mission", "Drive", "Agency",
    "Judgment", "Incisiveness", "Curiosity",
    "Positivity", "Resilience", "Growth Mindset",
    "Compelling Impact", "Connection", "Environmental Insight"
]
personal_ratings = {trait: st.selectbox(trait, rating_scale, key=f"personal_{trait}") for trait in personal_traits}

st.subheader("B. Leadership Capabilities")
capability_traits = [
    "Achieves Sustainable Impact", "Creates Focus", "Orchestrates Delivery",
    "Frames Complexity", "Identifies New Possibilities", "Generates Solutions",
    "Inspires People", "Drives Culture", "Grows Self and Others",
    "Aligns Stakeholders", "Models Collaboration", "Builds Teams"
]
capability_ratings = {trait: st.selectbox(trait, rating_scale, key=f"cap_{trait}") for trait in capability_traits}

# === Summary Ratings (green balls) ===
st.subheader("C. Summary Judgments")
overall_categories = ["Fit for Role", "Capabilities", "Potential", "Future Considerations"]
overall_ratings = {cat: st.selectbox(cat, rating_scale, key=f"overall_{cat}") for cat in overall_categories}

# === Reasoning Scores ===
st.subheader("D. Reasoning Scores (1–99%)")
verbal_score = st.number_input("Verbal", min_value=1, max_value=99, value=70)
numerical_score = st.number_input("Numerical", min_value=1, max_value=99, value=70)
abstract_score = st.number_input("Abstract", min_value=1, max_value=99, value=70)
overall_reasoning = st.number_input("Overall", min_value=1, max_value=99, value=70)

# === Generate Report ===
st.header("4. Generate Report")
if st.button("Generate Full PowerPoint Report"):
    if not notes.strip() or not candidate_name or not role_and_company:
        st.warning("Please complete candidate info and notes before generating the report.")
    else:
        with st.spinner("Generating report with GPT-4o and formatting your PowerPoint..."):
            try:
                # === Call GPT-4o ===
                ai_report = generate_report(notes)

                # TEMPORARY placeholders (to be extracted from ai_report)
                personal_profile = "This is a sample personal profile."
                strengths = [
                    {"title": "Strategic Vision", "paragraph": "Can define and drive strategy."},
                    {"title": "Empathy", "paragraph": "Connects well with others."},
                    {"title": "Decisiveness", "paragraph": "Makes quick, confident choices."},
                ]
                development_areas = [
                    {"title": "Delegation", "paragraph": "Could improve task sharing."},
                    {"title": "Adaptability", "paragraph": "Needs to adjust to change more fluidly."},
                    {"title": "Data Fluency", "paragraph": "More confidence using data needed."},
                ]
                future_considerations = "Aims to become Regional Director with strong potential."

                # === Generate PowerPoint ===
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
                    ppt_path = tmp.name

                build_report_pptx(
                    template_path="templates/Template of Report.pptx",
                    output_path=ppt_path,
                    candidate_name=candidate_name,
                    role_and_company=role_and_company,
                    personal_profile=personal_profile,
                    strengths=strengths,
                    development_areas=development_areas,
                    future_considerations=future_considerations
                )

                with open(ppt_path, "rb") as f:
                    st.success("✅ Report generated successfully!")
                    st.download_button("📅 Download PowerPoint", f, file_name="Leadership_Report.pptx")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
