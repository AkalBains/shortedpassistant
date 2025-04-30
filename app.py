import streamlit as st
from utils.openai_api import generate_report
from utils.ppt_builder import build_report_pptx
from string import Template
import tempfile
import os

# ✅ Set page config (must be first Streamlit command)
st.set_page_config(page_title="Leadership Report Generator", layout="centered")

# 🔐 Simple password protection
PASSWORD = st.secrets.get("APP_PASSWORD", "changeme")

def check_password():
    st.title("🔒 Leadership Report Generator Login")
    password = st.text_input("Enter the password:", type="password")
    if password == PASSWORD:
        return True
    elif password:
        st.error("Incorrect password. Please try again.")
        return False
    return False

if not check_password():
    st.stop()

# 🧠 App main content after successful login
st.title("🧠 Leadership Consulting Report Generator")
st.markdown("Enter consultant notes, ratings, and identity details below to generate a full report.")

# === Section 1: Consultant Notes ===
st.header("1. Consultant Notes")
notes = st.text_area(
    label="Paste the consultant notes here:",
    placeholder="Include Personal Profile, Strengths, Development Areas, Future Considerations",
    height=300
)

# === Section 2: Candidate Details ===
st.header("2. Candidate Details")
candidate_name = st.text_input("Candidate Name")
role_and_company = st.text_input("Role and Company")

# === Section 3: Generate PowerPoint ===
st.header("3. Generate PowerPoint Report")

if st.button("Generate Full Report"):
    if not notes.strip() or not candidate_name or not role_and_company:
        st.warning("Please fill in candidate name, role/company, and consultant notes.")
    else:
        with st.spinner("Generating report with GPT-4o..."):
            try:
                # === Call GPT to generate report text ===
                ai_report = generate_report(notes)

                # === TEMP placeholder breakdown ===
                # These would be parsed out from ai_report text later
                personal_profile_text = "This is a sample personal profile based on the individual's psychological drivers and motivational patterns."
                strengths = [
                    {"title": "Strategic Vision", "paragraph": "She can define and drive long-term strategy with clarity and confidence."},
                    {"title": "Empathy", "paragraph": "She demonstrates strong interpersonal awareness and connects authentically with others."},
                    {"title": "Decisiveness", "paragraph": "She makes informed decisions quickly, especially under pressure."},
                ]
                development_areas = [
                    {"title": "Delegation", "paragraph": "Could benefit from distributing tasks more effectively across the team."},
                    {"title": "Adaptability", "paragraph": "Sometimes struggles when priorities shift rapidly in high-change environments."},
                    {"title": "Data Fluency", "paragraph": "Needs to build greater comfort in using data for decision-making."},
                ]
                future_considerations = "She aspires to take on a Regional Director role and shows strong potential with the right mentoring and visibility."

                # === Build and save PowerPoint ===
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
                    ppt_path = tmp.name

                build_report_pptx(
                    template_path="templates/Template of Report.pptx",
                    output_path=ppt_path,
                    candidate_name=candidate_name,
                    role_and_company=role_and_company,
                    personal_profile=personal_profile_text,
                    strengths=strengths,
                    development_areas=development_areas,
                    future_considerations=future_considerations
                )

                # === Download button ===
                with open(ppt_path, "rb") as f:
                    st.success("✅ PowerPoint report generated successfully!")
                    st.download_button("📥 Download PowerPoint", f, file_name="Leadership_Report.pptx")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

