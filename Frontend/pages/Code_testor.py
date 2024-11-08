import streamlit as st
import os
from pathlib import Path

# Page setup
st.set_page_config(page_title="Project Display Page", layout="centered")

st.title("Display Submitted Project Information")

# Check if project details exist in session state
if "project_title" in st.session_state and "project_description" in st.session_state:
    # Display the project title and description in code-style format
    st.subheader("Project Information")
    st.code(f"Title: {st.session_state.project_title}\n\nDescription:\n{st.session_state.project_description}", language="markdown")
else:
    st.warning("No project information submitted yet. Please go to the main page to enter the details.")

# Folder where the zip file is stored
zip_folder = Path("D:/Downloads/genMaya/zip_files")
zip_files = list(zip_folder.glob("*.zip"))  


if zip_files:
    for zip_file in zip_files:
        st.subheader(f"Available Zip File: {zip_file.name}")
        
        
        with open(zip_file, "rb") as file:
            btn = st.download_button(
                label="Download Zip File",
                data=file,
                file_name=zip_file.name,
                mime="application/zip"
            )
else:
    st.warning("No zip file found in the specified folder.")
