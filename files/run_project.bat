@echo on

REM Save the old environment, deactivate it if active
set OLD_ENV=%VIRTUAL_ENV%
if defined VIRTUAL_ENV (
    call %VIRTUAL_ENV%\Scripts\deactivate
)

REM Navigate to the project directory and set up the new environment
cd /d D:\Downloads\genMaya\projects\%1
echo Now in directory: %cd%

set NEW_ENV_NAME=proj
set NEW_ENV_PATH=%cd%\%NEW_ENV_NAME%
python -m venv %NEW_ENV_PATH%

REM Activate the new environment and run installation commands inline
call %NEW_ENV_PATH%\Scripts\activate && (
    cd ..\src
    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        echo "requirements.txt not found. No packages were installed."
    )

    pip uninstall werkzeug -y
    pip install werkzeug==2.2.2
    pip install flask
    pip install requests
)
python D:/Downloads/genMaya/projects/krishna/src/app.py
echo Environment setup complete.
