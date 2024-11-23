import streamlit as st
import os
from pathlib import Path
import requests
import os
import subprocess

st.set_page_config(page_title="Project Display Page", layout="centered")

st.title("Display Submitted Project Information")

# Display project information
if "project_title" in st.session_state and "project_description" in st.session_state:
    st.subheader("Project Information")
    st.code(f"Title: {st.session_state.project_title}\n\nDescription:\n{st.session_state.project_description}", language="markdown")
else:
    st.warning("No project information submitted yet. Please go to the main page to enter the details.")

# List available zip files
zip_folder = Path("D:/Downloads/genMaya/zip_files")
zip_files = list(zip_folder.glob("*.zip"))

if zip_files:
    for zip_file in zip_files:
        if st.session_state.project_title in zip_file.name:
            st.subheader(f"Available Zip File: {zip_file.name}")
            
            # Provide download button for the zip file
            with open(zip_file, "rb") as file:
                st.download_button(
                    label="Download Zip File",
                    data=file,
                    file_name=zip_file.name,
                    mime="application/zip"
                )
            # subprocess.Popen(["python", "D:/Downloads/genMaya/projects/krishna/src/app.py"])
            
            # "Check Code" button
            if st.button("Check Code"):
                with st.spinner("Running code validation..."):
                    try:
                        # Execute val.py
                        response = requests.post('http://127.0.0.1:5000/code_val')
                        # If execution is successful, refresh and show success message
                        st.success("Code validation successful!")
                    except subprocess.CalledProcessError as e:
                        st.error(f"Code validation failed. Error: {e}")
