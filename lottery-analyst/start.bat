@echo off
rem Lottery Analyst launcher for Windows: double-click to start.
cd /d "%~dp0"
set PY=python
where py >nul 2>nul && set PY=py -3
%PY% --version >nul 2>nul || (
  echo Python 3 is not installed. Get it from https://www.python.org/downloads/ and run this again.
  pause
  exit /b 1
)
%PY% -c "import certifi" 2>nul || %PY% -m pip install certifi >nul 2>nul
%PY% -c "import numpy" 2>nul || %PY% -m pip install numpy || (
  echo Could not install numpy. Run:  %PY% -m pip install numpy
  pause
  exit /b 1
)
%PY% app.py
pause
