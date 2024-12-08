@echo on

REM Deactivate any active virtual environment
call Scripts\deactivate

cd /d D:\Downloads\genMaya

REM Reactivate the old environment if it exists
set OLD_ENV=env_3.12
if exist %OLD_ENV%\Scripts\activate (
    call %OLD_ENV%\Scripts\activate
) else (
    echo "No previous environment to reactivate."
)
