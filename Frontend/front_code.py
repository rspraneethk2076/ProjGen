import streamlit as st
import requests
import os
import time

import sys
sys.path.append("C:/Users/HP/Downloads/GenMaya3s/Llama_RAG")
from vectors import EmbeddingsManager
from chatbot import ChatbotManager  # Assuming you have chatbot.py for ChatbotManager

def raw_code(response, file_path):
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("Code has been saved as flask_app.txt")
        return True
    else:
        print("Failed to generate code:", response.status_code, response.text)
        return False

def show_logs():
    script_dir = os.path.dirname(__file__)  
    project_dir = os.path.dirname(script_dir)
    log_file_path = os.path.join(project_dir, 'genmaya3s.log')
    try:
        with open(log_file_path, "r") as file:
            log_data = file.read()
        st.sidebar.text_area("Log Output", value=log_data, height=300, max_chars=None)
    except IOError:
        st.sidebar.error("Failed to read log file.")

url = 'http://127.0.0.1:5000/generate_code'

# Page setup
st.set_page_config(page_title="Project Description App", layout="centered")

st.title("Project Description Input")

# Input fields for title and description
project_title = st.text_input("Project Title")
project_description = st.text_area("Project Description")

# File uploader for PDF
uploaded_pdf = st.file_uploader("Upload Project Description (PDF)", type="pdf")

# Initialize session state for the project details if not present
if "project_title" not in st.session_state:
    st.session_state.project_title = ""
if "project_description" not in st.session_state:
    st.session_state.project_description = ""
if "vector_db_status" not in st.session_state:
    st.session_state.vector_db_status = None
if "chatbot_manager" not in st.session_state:
    st.session_state['chatbot_manager'] = None
if "messages" not in st.session_state:
    st.session_state['messages'] = []

# Handle Submit button
if st.button("Submit"):
    if project_title and (project_description or uploaded_pdf):
        # Save the project details to session state
        st.session_state.project_title = project_title
        st.session_state.project_description = project_description

        # Prepare payload and files
        payload = {
            "problem_statement": st.session_state.project_description,
            "project_name": st.session_state.project_title
        }
        files = {"file": uploaded_pdf.getvalue()} if uploaded_pdf else None

        response = requests.post(url, json=payload, files=files)
        file_created = raw_code(response, file_path=os.path.join("C:/Users/HP/Downloads/GenMaya3s/files", f'{st.session_state.project_title}_flask_app.txt'))
        
        if file_created:
            st.success("Project information submitted.")
            st.write("Go to the **Display Page** in the sidebar to view the details.")
        else:
            st.warning("There is an issue in file creation")

# Add button for creating vector database
if uploaded_pdf and st.button("Create Vector DB"):
    temp_pdf_path = f"{project_title}_description.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())
    
    # Create embeddings and vector DB
    embeddings_manager = EmbeddingsManager(
        model_name="BAAI/bge-small-en",
        device="cpu",
        encode_kwargs={"normalize_embeddings": True},
        qdrant_url="http://localhost:6333",
        collection_name="vector_db"
    )
    
    with st.spinner("🔄 Creating vector database..."):
        try:
            result = embeddings_manager.create_embeddings(temp_pdf_path)
            st.session_state.vector_db_status = result
            st.success("✅ Vector DB successfully created for the document!")
            
            # Initialize ChatbotManager
            st.session_state['chatbot_manager'] = ChatbotManager(
                model_name="BAAI/bge-small-en",
                device="cpu",
                encode_kwargs={"normalize_embeddings": True},
                llm_model="llama3.2:3b",
                llm_temperature=0.7,
                qdrant_url="http://localhost:6333",
                collection_name="vector_db"
            )
        except Exception as e:
            st.session_state.vector_db_status = f"⚠️ An error occurred: {e}"
            st.error(st.session_state.vector_db_status)

# Chat with Document
st.header("💬 Chat with Document")

if st.session_state['chatbot_manager'] is None:
    st.info("🤖 Please upload a PDF and create embeddings to start chatting.")
else:
    # Display existing messages
    for msg in st.session_state['messages']:
        st.chat_message(msg['role']).markdown(msg['content'])

    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Display user message
        st.chat_message("user").markdown(user_input)
        st.session_state['messages'].append({"role": "user", "content": user_input})

        with st.spinner("🤖 Responding..."):
            try:
                # Get the chatbot response using the ChatbotManager
                answer = st.session_state['chatbot_manager'].get_response(user_input)
                time.sleep(1)  # Simulate processing time
            except Exception as e:
                answer = f"⚠️ An error occurred while processing your request: {e}"
        
        # Display chatbot message
        st.chat_message("assistant").markdown(answer)
        st.session_state['messages'].append({"role": "assistant", "content": answer})

# Sidebar for logs
st.sidebar.header("Project Logs")
show_logs()
