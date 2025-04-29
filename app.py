import streamlit as st
from utils.openai_api import generate_report
from string import Template
import os

# ✅ Must be first Streamlit call
st.set_page_config(page_title="Leadership Report Generator", layout="centered")

# --- Simple password protection ---
PASSWORD = st.secrets.get("APP_PASSWORD", "changeme")  # fallback

def check_password():
    st.title("🔒 Leadership Report Generator Login")
    password = st.text_input("Enter the password:", type="password")
    if password == PASSWORD:
        return True
    elif password:
        st.error("Incorrect password. Please try again.")
        return False
    else:
        return False

if not check_password():
    st.stop()

# --- Main app content after successful login ---
st.title("🧠 Leadership Consulting Report Generator")
st.markdown("Enter the consultant notes and ratings below to generate a full report.")

# --- Consultant Notes Input ---
st.header("1. Consultant Notes")
notes = st.text_area(
    label="Paste the consultant notes here:",
    placeholder="Include sections like Personal Profile, Strengths, Development Areas, Future Considerations",
    height=300
)

# --- Ratings Input ---
st.header("2. Ratings")
st.markdown("Optional: Use sliders to provide ratings.")

ratings = {
    "Leadership": st.slider("Leadership", 1, 5, 3),
    "Communication": st.slider("Communication", 1, 5, 3),
    "Strategic Thinking": st.slider("Strategic Thinking", 1, 5, 3),
    "Emotional Intelligence": st.slider("Emotional Intelligence", 1, 5, 3),
}

# --- Load Report Template ---
try:
    with open("report_template.txt", "r") as file:
        template_str = file.read()
        template = Template(template_str)
except FileNotFoundError:
    st.error("❌ Could not find report_template.txt. Please add it to the root of the project.")
    st.stop()

# --- Generate Report Button ---
st.header("3. Generate Report")
if st.button("Generate Full Report"):
    if not notes.strip():
        st.warning("Please enter consultant notes before generating the report.")
    else:
        with st.spinner("Generating report with GPT-4o..."):
            try:
                ai_report = generate_report(notes)

                # Merge ratings and AI report into template
                final_report = template.substitute(
                    notes=notes,
                    ai_report=ai_report,
                    leadership=ratings["Leadership"],
                    communication=ratings["Communication"],
                    strategic=ratings["Strategic Thinking"],
                    emotional=ratings["Emotional Intelligence"]
                )

                st.success("✅ Report generated successfully!")
                st.text_area("📄 Final Report", final_report, height=500)
                st.download_button("📥 Download Report", final_report, file_name="consulting_report.txt")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

