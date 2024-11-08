from langchain import HuggingFaceHub, LLMChain, PromptTemplate
import subprocess
from flask import Flask, request, jsonify, send_file
import os
import time
import threading




subprocess.run(["python", "login_hf.py"])

app = Flask(__name__)



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




if __name__ == '__main__':
    app.run(debug=True, port=5000)