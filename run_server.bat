@echo off
echo Attempting to run Django server...

REM Try different Python paths
echo Trying venv Python...
venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

echo.
echo If above failed, trying system Python...
python manage.py runserver 127.0.0.1:8000

pause
