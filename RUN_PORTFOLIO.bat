@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  echo Install Python 3 from https://www.python.org/downloads/ and select "Add Python to PATH".
  pause
  exit /b 1
)

python -c "import flask" >nul 2>nul
if errorlevel 1 (
  echo Installing Flask for the local portfolio...
  python -m pip install Flask==3.1.2
  if errorlevel 1 (
    echo Flask installation failed. Check your internet connection and try again.
    pause
    exit /b 1
  )
)

echo Starting the portfolio at http://127.0.0.1:5000/
start "Portfolio Flask Server" /min python -m flask --app app run --no-debugger --no-reload --host 127.0.0.1 --port 5000
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5000/"

echo.
echo The portfolio has been opened in your browser.
echo Keep the "Portfolio Flask Server" window open while testing the contact form.
echo Close that server window when you finish.
pause
