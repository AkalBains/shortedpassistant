import streamlit as st
from utils.openai_api import generate_report
from string import Template

st.title("Leadership Consulting Report Generator")

# Consultant notes
notes = st.text_area("Consultant Notes")

# Example rating inputs
ratings = {
    "Leadership": st.slider("Leadership Rating", 1, 5, 3),
    "Communication": st.slider("Communication Rating", 1, 5, 3),
    "Strategic Thinking": st.slider("Strategic Thinking Rating", 1, 5, 3)
}

# Upload template (or load from file)
template_str = open("report_template.txt").read()
template = Template(template_str)

if st.button("Generate Report"):
    with st.spinner("Generating report..."):
        ai_report = generate_report(notes)
        final_report = template.substitute(
            notes=notes,
            ai_report=ai_report,
            leadership=ratings["Leadership"],
            communication=ratings["Communication"],
            strategic=ratings["Strategic Thinking"]
        )
        st.text_area("Final Report", final_report, height=400)
        st.download_button("Download Report", final_report, file_name="report.txt")
