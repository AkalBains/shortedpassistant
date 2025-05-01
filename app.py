import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from ppt_builder import create_powerpoint
from radar_charts import generate_radar_charts
from trait_scores import process_traits
from openai_api import generate_report

# 🔧 Configure Streamlit page – must be FIRST Streamlit command
st.set_page_config(page_title="Leadership Report Generator", layout="wide")

# 🌐 Load environment variables
load_dotenv()

# 🧠 App Title
st.title("🧾 Leadership Report Generator")

# 📤 File uploader for CSV input
uploaded_file = st.file_uploader("Upload CSV file with leadership assessment data", type=["csv"])

# 💡 When file is uploaded, process it
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file loaded successfully!")
        st.dataframe(df.head())

        # 🧮 Step 1: Process trait scores
        trait_data = process_traits(df)
        st.subheader("Trait Scores")
        st.dataframe(trait_data)

        # 📊 Step 2: Generate radar charts
        radar_imgs = generate_radar_charts(trait_data)

        # ✍️ Step 3: Generate AI-powered leadership report
        st.subheader("Generating Leadership Report...")
        report_text = generate_report(trait_data)
        st.text_area("Leadership Report", value=report_text, height=300)

        # 📽 Step 4: Build PowerPoint presentation
        pptx_file = create_powerpoint(trait_data, radar_imgs, report_text)

        # 📥 Allow download
        st.subheader("Download PowerPoint")
        st.download_button(
            label="📥 Download Presentation",
            data=pptx_file,
            file_name="leadership_report.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV file to begin.")
