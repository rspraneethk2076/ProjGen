from langchain import HuggingFaceHub, LLMChain, PromptTemplate
import subprocess
from flask import Flask, request, jsonify, send_file
import os
import time
import threading
import streamlit as st
import requests
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_function import logger


subprocess.run(["python", "login_hf.py"])
logger.debug("login_hf.py script executed")

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
app = Flask(__name__,template_folder='C:/Users/HP/Downloads/GenMaya3s/projects/project1/templates')
import logging
import traceback
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    filemode='w',  
)

@app.errorhandler(Exception)
def handle_error(e):

    app.logger.error(f"Exception occurred: {{traceback.format_exc()}}")

    return "Internal Server Error", 500


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
app = Flask(__name__,template_folder='C:/Users/HP/Downloads/GenMaya3s/projects/project1/templates')
app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
counter = 0

import logging
import traceback
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    filemode='w',  
)

@app.errorhandler(Exception)
def handle_error(e):

    app.logger.error(f"Exception occurred: {{traceback.format_exc()}}")

    return "Internal Server Error", 500

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
logger.info("HuggingFaceHub and LLMChain initialized")

chain = LLMChain(llm=llm, prompt=prompt_template)


@app.route('/')
def home():
    logger.debug("Home route accessed")
    return "Server is running", 200

@app.route('/generate_code', methods=['POST'])
def generate_code():
    # Retrieve the problem statement from the request
    logger.debug("Accessed /generate_code endpoint.")
    data = request.get_json()
    problem_statement = data.get('problem_statement', '')
    project_name=data.get('project_name','')
    logger.info(f"Received data - Problem Statement: {problem_statement}, Project Name: {project_name}")
    # Use the problem statement to invoke the model
    try:
        response = chain.invoke({'problem_statement': problem_statement})
        formatted_code = response['text'].strip()
        logger.info("Code generated successfully by the model.")
    except Exception as e:
        logger.error("Failed to generate code with the model.", exc_info=True)
        return jsonify({"error": "Failed to generate code"}), 500

    file_path = os.path.join("C:/Users/HP/Downloads/GenMaya3s/files",f'{project_name}_flask_app.txt')
    try:
        with open(file_path, 'w') as file:
            file.write(formatted_code)
        logger.info(f"Code written to file successfully: {file_path}")
    except IOError as e:
        logger.error(f"Failed to write to file: {file_path}", exc_info=True)
        return jsonify({"error": "Failed to write to file"}), 500

    time.sleep(5)
    logger.debug('Processing completed with a delay for file handling')
    # bat_file_path = os.path.join("C:/Users/HP/Downloads/GenMaya3s", "main.bat")  # Update with your actual path
    # subprocess.run([bat_file_path], shell=True)


    try:
        subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_encode/remove_noise.py", project_name], shell=True)
        subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_encode/format_folders.py", project_name], shell=True)
        logger.info("Subprocesses for removing noise and formatting folders completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error("Subprocess execution failed.", exc_info=True)
        return jsonify({"error": "Subprocess execution failed"}), 500
    # Return the file to the client
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error("Failed to send file to client.", exc_info=True)
        return jsonify({"error": "Failed to send file"}), 500


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
    
    Example 1 :
    The final Code:
    
    #src/app.py
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__,template_folder='C:/Users/HP/Downloads/GenMaya3s/projects/project1/templates')



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
app = Flask(__name__,template_folder='C:/Users/HP/Downloads/GenMaya3s/projects/project1/templates')
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

# @app.route('/correct_code',methods=['POST'])
# def correct_code():



#     data = request.get_json()
#     error_message=data.get('project_name','')
#     problem_statement, project_name = st.session_state.project_description, st.session_state.project_title
#     with open(f"C:/Users/HP/Downloads/GenMaya3s/files/{project_name}_flask_app.txt", 'r') as file:
#         existing_code = file.read()

#     chain= correct_error(error_message,existing_code,problem_statement)

#     response = chain.invoke({'problem_statement': problem_statement,'existing_code':existing_code,'error_message':error_message })

#     formatted_code = response['text'].strip()

#     file_path = os.path.join("C:/Users/HP/Downloads/GenMaya3s/files",f'{project_name}_flask_app.txt')
#     with open(file_path, 'w') as file:
#         file.write(formatted_code)

#     time.sleep(5)
#     # bat_file_path = os.path.join("C:/Users/HP/Downloads/GenMaya3s", "main.bat")  # Update with your actual path
#     # subprocess.run([bat_file_path], shell=True)


#     subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_encode/remove_noise.py",project_name], shell=True)
#     subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_encode/format_folders.py",project_name], shell=True)

#     return send_file(file_path, as_attachment=True)




def get_last_log_lines(log_file, num_lines=4):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
            logger.info(f"Successfully retrieved last lines from {log_file}")
            return lines[-num_lines:]  # Return the last 'num_lines' lines
    except FileNotFoundError:
        logger.error(f"Log file not found: {log_file}")
        return ["Log file not found.\n"]
    except Exception as e:
        logger.error(f"Error reading log file {log_file}: {str(e)}", exc_info=True)
        return [f"Error reading log file: {e}\n"]

# Function to test routes and capture logs
def test_routes(routes, log_file="C:/Users/HP/Downloads/GenMaya3s/Frontend/app.log"):
    logs_per_route = {}

    for route in routes:
        url = f"{route}"
        logger.debug(f"Testing route: {url}")

        try:
            response = requests.get(url)
            status_code = response.status_code
            logger.info(f"Request to {url} returned status code {status_code}")
        except Exception as e:
            logger.error(f"Error requesting {url}: {str(e)}", exc_info=True)
            status_code = None
        
        # Fetch the last 4 lines of the log file
        last_log_lines = get_last_log_lines(log_file)
        logs_per_route[route] = "".join(last_log_lines)  

    return str(logs_per_route)



@app.route('/correct_code', methods=['POST'])
def correct_code():
    logger.debug("Accessed the correct_code endpoint")
    data = request.get_json()
    error_message = data.get('error_message', '')
    problem_statement = "You are tasked with creating a basic web application using Flask that functions as a simple counter application. The application should have buttons for incrementing and decrementing a counter value. The current value of the counter should be displayed prominently on the page and updated dynamically as the user interacts with the buttons. Additionally, a reset button should be included to reset th"
    project_name = "krishna"
    logger.info(f"Received data for project {project_name} with error message: {error_message}")
    # Read the existing code from the file
    file_path = f"C:/Users/HP/Downloads/GenMaya3s/files/{project_name}_flask_app.txt"
    try:
        with open(file_path, 'r') as file:
            existing_code = file.read()
        logger.info(f"Successfully read existing code from {file_path}")
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to read file"}), 500

    # Correct the error by invoking the LLM chain
    try:
        chain = correct_error()  # Assume correct_error returns a configured LLMChain instance
        response = chain.invoke({
            'problem_statement': problem_statement,
            'existing_code': existing_code,
            'error_details': error_message
        })
        formatted_code = response['text'].strip()
        logger.debug("Code correction invoked successfully")
    except Exception as e:
        logger.error("Failed during LLM chain invocation", exc_info=True)
        return jsonify({"error": "LLM chain invocation failed"}), 500

    try:
        with open(file_path, 'w') as file:
            file.write(formatted_code)
        logger.info(f"Corrected code written successfully to {file_path}")
    except Exception as e:
        logger.error(f"Failed to write to file {file_path}: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to write to file"}), 500

    time.sleep(5)
    try:
        subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_encode/remove_noise.py", project_name], shell=True)
        subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_encode/format_folders.py", project_name], shell=True)
        logger.info("Post-correction subprocesses executed successfully")
    except subprocess.CalledProcessError as e:
        logger.error("Subprocess execution failed", exc_info=True)
        return jsonify({"error": "Subprocess execution failed"}), 500
    time.sleep(10)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error("Failed to send file to client", exc_info=True)
        return jsonify({"error": "Failed to send file"}), 500



def get_routes_from_app(file_path):
    route_pattern = re.compile(r"@app\.route\(['\"](.*?)['\"].*?\)")
    routes = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = route_pattern.search(line)
                if match:
                    routes.append(f"http://127.0.0.1:5001{match.group(1)}")
        logger.info("Detected routes: {}".format(routes))
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []  # Return an empty list if the file cannot be found
    except Exception as e:
        logger.error(f"An error occurred while reading the file {file_path}: {str(e)}")
        return []
    return routes

@app.route('/code_val',methods=['POST'])
def code_validator():
    data=request.get_json()
    project_name=data.get('project_name','')
    app_file_path = f"C:/Users/HP/Downloads/GenMaya3s/projects/{project_name}/src/app.py"
    # batch_file_path = "C:/Users/HP/Downloads/GenMaya3s/projects/krishna/run_project.bat"
    # batch_args = ["krishna"]
    api_endpoints = get_routes_from_app(app_file_path)

    print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
    # Run setup batch script and wait for it to complete
    # subprocess.Popen([batch_file_path] + batch_args, shell=True)
    # print("Environment setup complete")

    # # Start the Flask app in a separate process

    # # out,err=app_process.communicate()
    # time.sleep(6)


    try:
        
        # response = requests.get(endpoint)
        # if response.status_code != 200:
        #     print(f"Error at {endpoint}: Status {response.status_code}")
            
            # # Terminate the Flask app process and re-run the setup
            # subprocess.run(["C:/Users/HP/Downloads/GenMaya3s/start_proj.bat"], shell=True, check=True)
            # time.sleep(5)

            # Run error handler with the error response
   # Extract up to 200 characters of error
            error_details=test_routes(api_endpoints)
            # subprocess.run(["python", "C:/Users/HP/Downloads/GenMaya3s/Code_Corrector/Code.py", error_details], shell=True, check=True)
            payload = {
        "error_message": error_details
            }
            response=requests.post("http://127.0.0.1:5000/correct_code",json=payload)
            time.sleep(5)
            logger.info("Post request to correct_code completed successfully")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request to correct_code failed: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
                 

    return "Flask app process terminated"



if __name__ == '__main__':
    app.run(debug=True, port=5000)