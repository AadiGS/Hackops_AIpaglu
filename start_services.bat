@echo off
echo Starting MoodTune AI Services...
echo.

echo Starting Backend API Server...
start "Backend API" cmd /k "cd backend && python start_server.py"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Development Server...
start "Frontend" cmd /k "cd frontend1 && npm run dev"

echo.
echo Both services are starting...
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
