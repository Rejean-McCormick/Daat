@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL%==0 (set PY=py -3) else (set PY=python)
%PY% -c "import sys; assert sys.version_info >= (3,10), 'Python >=3.10 required'" || exit /b 1
%PY% -m pip install -e ".[dev]" || exit /b 1
%PY% -m daat verify-contracts || exit /b 1
%PY% -m daat alignment-report mappings\native\profile.json || exit /b 1
%PY% -m daat alignment-report mappings\foreign-inventory\profile.json || exit /b 1
%PY% -m pytest -q || exit /b 1
echo DaaT local validation complete. No service has been started.
pause
