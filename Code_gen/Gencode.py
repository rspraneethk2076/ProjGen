from langchain import HuggingFaceHub, LLMChain, PromptTemplate
import subprocess
from flask import Flask, request, jsonify, send_file
import os
import time
import threading
import streamlit as st
import requests
import re



subprocess.run(["python", "login_hf.py"])

app = Flask(__name__)
existing_code=""


prompt_template = PromptTemplate.from_template(
    '''
    Given the following problem statement, generate all the required files and their content for a very very mini simple Flask project Not so complexed and large codes:

    Problem statement: {problem_statement}

    Generate the output in markdown format with each file including its path. Use the following structure for each file:
    #DirectoryName/FileName
    <code>

    Ensure the following strict format:
    1. Each file should start with #DirectoryName/FileName on its own line.
    2. Immediately follow this with the corresponding code without any extra text, comments, or lines.
    3. There should be absolutely no comments or additional text in the response—only file paths and their respective code.
    4. There should very very mini simple Flask project Not so complexed and large codes.
    5. Only one set of codes is required strictly
  

    Include only files that are necessary for the solution to the problem statement, with directories in the paths (e.g., templates/login.html, src/app.py, src/requirements.txt etc...) where relevant. Also, make sure to include:
    - A requirements.txt file listing all dependencies.
    - A batch file (run_project.bat) that contains the necessary commands to run the Flask project.
    - Secret key can be your own random 24 chars string
    - The main routing should be always only '/'
    - Remember in src/app.py main method is must and sure.
    - Make sur html is as small as possible . it is high preiority
    - Just you need to take structure from the example not the logic. please remember that
    - Dont keep templates inside src

    
    Example 1 :
    The final Code:
    
    #src/app.py
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__,template_folder='D:/Downloads/genMaya/projects/project1/templates')


app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate user logic here
        return redirect(url_for('home'))
    return render_template('login.html')
    
if __name__ == '__main__':
    app.run(debug=True)

#templates/login.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <form action="/login" method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>

#src/requirements.txt
Flask==2.0.3


#src/run_project.bat
@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=src/app.py
set FLASK_ENV=development
flask run
pause


Example 2:

The final Code:
  
#src/app.py
from flask import Flask, render_template, jsonify
app = Flask(__name__,template_folder='D:/Downloads/genMaya/projects/project1/templates')
app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
counter = 0

@app.route('/counter', methods=['GET'])
def get_counter():
    return jsonify(counter=counter)

@app.route('/increment', methods=['POST'])
def increment():
    global counter
    counter += 1
    return jsonify(counter=counter)

@app.route('/decrement', methods=['POST'])
def decrement():
    global counter
    counter -= 1
    return jsonify(counter=counter)

if __name__ == '__main__':
    app.run(debug=True)
    
#templates/counter.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Counter</title>
</head>
<body>
    <h1>Counter: <span id="counter">0</span></h1>
    <button onclick="increment()">Increment</button>
    <button onclick="decrement()">Decrement</button>
</body>
</html>


#src/requirements.txt
Flask==2.0.3


#src/run_project.bat
@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=src/app.py
set FLASK_ENV=development
flask run
pause
    '''
)

llm = HuggingFaceHub(
    huggingfacehub_api_token="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",
    repo_id="meta-llama/Llama-3.2-3B-Instruct",
    model_kwargs={
        "device": 0,
        "max_new_tokens": 1000
    }
)

chain = LLMChain(llm=llm, prompt=prompt_template)


@app.route('/')
def home():
    return "Server is running", 200

@app.route('/generate_code', methods=['POST'])
def generate_code():
    # Retrieve the problem statement from the request
    data = request.get_json()
    problem_statement = data.get('problem_statement', '')
    project_name=data.get('project_name','')

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


################################################################

def correct_error():


    prompt_template = PromptTemplate.from_template(
        '''
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

    # Define LLM and chain
    llm = HuggingFaceHub(
        huggingfacehub_api_token="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",
        repo_id="meta-llama/Llama-3.2-3B-Instruct",
        model_kwargs={
            "device": 0,
            "max_new_tokens": 1000
        }
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain

@app.route('/correct_code',methods=['POST'])
def correct_code():



    data = request.get_json()
    error_message=data.get('project_name','')
    problem_statement, project_name = st.session_state.project_description, st.session_state.project_title
    with open(f"D:/Downloads/genMaya/files/{project_name}_flask_app.txt", 'r') as file:
        existing_code = file.read()

    chain= correct_error(error_message,existing_code,problem_statement)

    response = chain.invoke({'problem_statement': problem_statement,'existing_code':existing_code,'error_message':error_message })

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


def get_routes_from_app(file_path):
    route_pattern = re.compile(r"@app\.route\(['\"](.*?)['\"].*?\)")
    routes = []
    with open(file_path, 'r') as file:
        for line in file:
            match = route_pattern.search(line)
            if match:
                routes.append(f"http://127.0.0.1:8080{match.group(1)}")
    print("Detected routes:", routes)
    return routes

@app.route('/code_val',methods=['POST'])
def code_validator():
    app_file_path = "D:/Downloads/genMaya/projects/krishna/src/app.py"
    batch_file_path = "D:/Downloads/genMaya/projects/krishna/run_project.bat"
    batch_args = ["krishna"]

    


    api_endpoints = get_routes_from_app(app_file_path)


    print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
    # Run setup batch script and wait for it to complete
    subprocess.Popen([batch_file_path] + batch_args, shell=True)
    print("Environment setup complete")

    # Start the Flask app in a separate process
    
    # out,err=app_process.communicate()
    time.sleep(6)

    try:
        for endpoint in api_endpoints:
            try:
                response = requests.get(endpoint)
                if response.status_code != 200:
                    print(f"Error at {endpoint}: Status {response.status_code}")
                    
                    # # Terminate the Flask app process and re-run the setup
                    # subprocess.run(["D:/Downloads/genMaya/start_proj.bat"], shell=True, check=True)
                    # time.sleep(5)

                    # Run error handler with the error response
                    error_details = response.text[:200]  # Extract up to 200 characters of error
                    # subprocess.run(["python", "D:/Downloads/genMaya/Code_Corrector/Code.py", error_details], shell=True, check=True)
                    payload = {
                "error_message": error_details
                    }
                    response=requests.post("http://127.0.0.1:5000/correct_code",json=payload)
                    time.sleep(5)

                else:
                    print(f"{endpoint} responded successfully with status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request exception at {endpoint}: {e}")
                break  
    finally:
        
        print("Flask app process terminated")



if __name__ == '__main__':
    app.run(debug=True, port=5000)