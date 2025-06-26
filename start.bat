@echo off
echo Starting MediVerse Application...
echo.

echo Starting Backend Server...
start "MediVerse Backend" cmd /k "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start "MediVerse Frontend" cmd /k "cd frontend && npm start"

echo.
echo MediVerse is starting up!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul 