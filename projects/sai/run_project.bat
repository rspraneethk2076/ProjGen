@echo on

REM Save the old environment, deactivate it if active
@REM set OLD_ENV=%VIRTUAL_ENV%
@REM if defined VIRTUAL_ENV (
@REM     call %VIRTUAL_ENV%\Scripts\deactivate
@REM )

REM Navigate to the project directory and set up the new environment
cd /d D:\Downloads\genMaya\projects\%1\src
echo Now in directory: %cd%

@REM set NEW_ENV_NAME=proj
@REM set NEW_ENV_PATH=%cd%\%NEW_ENV_NAME%
@REM python -m venv %NEW_ENV_PATH%

@REM REM Activate the new environment and run installation commands inline
@REM call %NEW_ENV_PATH%\Scripts\activate && (
@REM     cd ..\src
@REM     if exist requirements.txt (
        
@REM     ) else (
@REM         echo "requirements.txt not found. No packages were installed."
@REM     )


@REM )
pip install -r requirements.txt
pip uninstall werkzeug -y
pip install werkzeug==2.2.2
pip install flask
pip install requests
@REM flask --app D:/Downloads/genMaya/projects/krishna/src/app.py run --host=127.0.0.1 --port=5001
echo Environment setup complete.
