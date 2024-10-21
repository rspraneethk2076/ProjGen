cd proj
call Scripts\activate
cd ..\src
pip install -r requirements.txt
pip uninstall werkzeug
pip install werkzeug==2.2.2
python app.py
