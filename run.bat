@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto :error
start "" ".venv\Scripts\pythonw.exe" app.py
powershell -NoProfile -Command "$ready=$false; for($i=0;$i -lt 20;$i++){try{if((Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:5000/health' -TimeoutSec 1).StatusCode -eq 200){$ready=$true; break}}catch{}; Start-Sleep -Milliseconds 500}; if(-not $ready){exit 1}"
if errorlevel 1 (
  echo PromptForge did not become ready at http://127.0.0.1:5000.
  echo Close any other app using port 5000, then try again.
  pause
  exit /b 1
)
start "" http://127.0.0.1:5000
exit /b 0

:error
echo PromptForge could not start. Check that Python 3 is installed and try again.
pause
exit /b 1
