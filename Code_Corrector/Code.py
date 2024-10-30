from langchain import HuggingFaceHub, LLMChain, PromptTemplate
import subprocess

# Run login script
subprocess.run(["python", "login_hf.py"])

problem_statement = '''
Create a Flask web app functioning as a scientific calculator. It should have an input field for mathematical expressions, support for basic arithmetic, trigonometric, and logarithmic functions, and handle errors like division by zero with error messages. The app should update results dynamically without page refresh, aiming for simplicity and real-time feedback.
'''

error_message = '''
Traceback (most recent call last):
  File "D:/Downloads/genMaya/Code_encode/format_folders.py", line 110, in <module>
    clean_requirements("D:/Downloads/genMaya/projects/project1/src/requirements.txt")
FileNotFoundError: [Errno 2] No such file or directory: 'D:/Downloads/genMaya/projects/project1/src/requirements.txt'
'''

# Reading existing code
with open("D:/Downloads/genMaya/files/flask_app.txt", 'r') as file:
    existing_code = file.read()

# Prompt template
prompt_template = PromptTemplate.from_template(
    f'''
Given a problem statement, existing code, and an error message below, correct and simplify the code as needed.

Problem statement: {problem_statement}
Existing code: {existing_code}
Error message: {error_message}

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

# Generate corrected code
response = chain.invoke({})
formatted_code = response['text'].strip()

# Save corrected code to file
with open('D:/Downloads/genMaya/files/flask_app.txt', 'w') as file:
    file.write(formatted_code)

print("Code has been saved as flask_app.txt")
