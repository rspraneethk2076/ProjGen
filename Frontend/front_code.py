import streamlit as st
import requests
import os
def raw_code(response,file_path):
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("Code has been saved as flask_app.txt")
        return True
    else:
        print("Failed to generate code:", response.status_code, response.text)
        return False



url = 'http://127.0.0.1:5000/generate_code'
# Page setup
st.set_page_config(page_title="Project Description App", layout="centered")

st.title("Project Description Input")

# Input fields for title and description
project_title = st.text_input("Project Title")
project_description = st.text_area("Project Description")

# Initialize session state for the project details if not present
if "project_title" not in st.session_state:
    st.session_state.project_title = ""
if "project_description" not in st.session_state:
    st.session_state.project_description = ""


if st.button("Submit"):
    if project_title and project_description:
        # Save the project details to session state
        st.session_state.project_title = project_title
        st.session_state.project_description = project_description

        payload = {
        "problem_statement": st.session_state.project_description,
        "project_name": st.session_state.project_title
        }
        response = requests.post(url, json=payload)
        file_created=raw_code(response,file_path = os.path.join("D:/Downloads/genMaya/files",f'{st.session_state.project_title}_flask_app.txt'))
        if file_created:
            st.switch_page("pages/Code_testor.py")  # Reload the page to reflect changes

            st.success("Project information submitted.")
            st.write("Go to the **Display Page** in the sidebar to view the details.")
        else:
            st.warning("There is issue in file creation")
