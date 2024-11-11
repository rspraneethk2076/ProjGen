import streamlit as st
import subprocess
import requests
from time import sleep
import os
import signal


server_url = "http://127.0.0.1:5000"
st.title("Flask Server Control Panel")
server_process =None


def check_server_status(url):
    try:
        response = requests.get(url, timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def start_server(st):

    subprocess.call(["flask", "--app", "D:/Downloads/genMaya/Code_gen/Gencode.py", "run"], shell=True)

def stop_server():
    subprocess.call("taskkill /f /im flask.exe", shell=True)
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
