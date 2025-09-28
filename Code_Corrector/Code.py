import subprocess
from langchain import HuggingFaceHub, LLMChain, PromptTemplate
import subprocess
from flask import Flask, request, jsonify, send_file
import os
import time
import threading
import streamlit as st
import argparse

# Run login script
# subprocess.run(["python", "login_hf.py"])

app = Flask(__name__)

problem_statement = '''
Create a Flask web app functioning as a scientific calculator. It should have an input field for mathematical expressions, support for basic arithmetic, trigonometric, and logarithmic functions, and handle errors like division by zero with error messages. The app should update results dynamically without page refresh, aiming for simplicity and real-time feedback.
'''

error_message = '''
Traceback (most recent call last):
  File "D:/Downloads/genMaya/Code_encode/format_folders.py", line 110, in <module>
    clean_requirements("D:/Downloads/genMaya/projects/project1/src/requirements.txt")
FileNotFoundError: [Errno 2] No such file or directory: 'D:/Downloads/genMaya/projects/project1/src/requirements.txt'
'''

with open("D:/Downloads/genMaya/files/flask_app.txt", 'r') as file:
    existing_code = file.read()




problem_statement= st.session_state.project_description
project_name= st.session_state.project_title

with open(f"D:/Downloads/genMaya/files/{project_name}_flask_app.txt", 'r') as file:
    existing_code = file.read()

def correct_error(error_details):


    prompt_template = PromptTemplate.from_template(
        f'''
    Given a problem statement, existing code, and an error message below, correct and simplify the code as needed.

    Problem statement: {problem_statement}
    Existing code: {existing_code}
    Error message: {error_details}

    Please output only the necessary corrected code in the following format:
    - For each file, start with the path in `#DirectoryName/FileName` format.
    - Directly follow with the code without any extra text, comments, or lines.
    - Only include essential files: `src/app.py`, `templates/index.html`, `src/requirements.txt`, and `src/run_project.bat`.
    - Minimal HTML and Flask code is preferred.

    Example format:

    #src/app.py
    <code>

    #templates/index.html
    <code>

    #src/requirements.txt
    <code>

    #src/run_project.bat
    <code>

    Ensure the `src/app.py` file uses a main route `'/'`, has a `main` method, and handles user inputs as per the problem statement. Avoid complex code, keep the HTML minimal, and make sure the `requirements.txt` file includes necessary dependencies.
    '''
    )
    from langchain_community.llms import Ollama

    llm = Ollama(
        model="llama3.2:3b",   # Change to the model you pulled with ollama pull
        base_url="http://localhost:11434",  # Default Ollama server
        temperature=0.7,
    )


    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain

@app.route('/correct_code',methods=['POST'])
def correct_code(error_message):
    # Retrieve the problem statement from the request
    data = request.get_json()
    problem_statement, project_name = st.session_state.project_description, st.session_state.project_title

    chain= correct_error({error_message})
    # Use the problem statement to invoke the model
    response = chain.invoke({'problem_statement': problem_statement})
    formatted_code = response['text'].strip()

    file_path = os.path.join("D:/Downloads/genMaya/files",f'{project_name}_flask_app.txt')
    with open(file_path, 'w') as file:
        file.write(formatted_code)

    time.sleep(5)
    # bat_file_path = os.path.join("D:/Downloads/genMaya", "main.bat")  # Update with your actual path
    # subprocess.run([bat_file_path], shell=True)


    subprocess.run(["python", "D:/Downloads/genMaya/Code_encode/remove_noise.py",project_name], shell=True)
    subprocess.run(["python", "D:/Downloads/genMaya/Code_encode/format_folders.py",project_name], shell=True)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True,port=5001)


