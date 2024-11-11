@echo on
if defined VIRTUAL_ENV (
    call %VIRTUAL_ENV%\Scripts\deactivate
)
cd /d D:\Downloads\genMaya\projects\%1
echo Now in directory: D:\Downloads\genMaya\projects\%1

python -m venv proj
cd proj
call Scripts\activate

cd ..\src
pip install -r requirements.txt

pip uninstall werkzeug -y
pip install werkzeug==2.2.2
pip install flask

echo Environment setup complete.
