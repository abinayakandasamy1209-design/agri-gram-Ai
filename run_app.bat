@echo off
title Agri Gram AI - Smart Farming Assistant
echo ========================================================
echo  🌾 Starting Agri Gram AI Server...
echo ========================================================
echo.

REM Open browser after 2 seconds
start "" http://127.0.0.1:5000

REM Run the application
python app.py
pause
