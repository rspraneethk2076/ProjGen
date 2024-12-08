import streamlit as st
import subprocess
import requests
from time import sleep
import os
import signal
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import PROJECTS_DIR
server_url = "http://127.0.0.1:5001"
st.title("Project Server Control Panel")
server_process =None


def check_server_status(url):
    try:
        response = requests.get(url, timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def start_server(st):
    batch_file_path = PROJECTS_DIR / 'krishna' / 'run_project.bat'
    batch_args = ["krishna"]
    
    # Run the batch script and wait for it to complete
    subprocess.run([batch_file_path] + batch_args, shell=True, check=True)
    print("Batch script executed successfully.")
    
    # Start the Flask server
    flask_app_path = PROJECTS_DIR / 'krishna' / 'src' / 'app.py'
    subprocess.run(
        ["flask", "--app", str(flask_app_path), "run", "--host=127.0.0.1", "--port=5001"],
        shell=False,
        check=True,
    )
    print("Flask server started successfully.")


def stop_server():
    subprocess.call("taskkill /f /im flask.exe", shell=False)
    sleep(2)

if st.button("Start Server"):
    start_server(st)

    


if st.button("Stop Server"):
    stop_server()
    st.warning("Server stopping...")


if st.button("Check Server Status"):
    is_running = check_server_status(server_url)
    

    if is_running:
        st.markdown(
            "<span style='color: green; font-size: 24px;'>⬤</span> Server is Running",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<span style='color: red; font-size: 24px;'>⬤</span> Server is Down",
            unsafe_allow_html=True
        )
