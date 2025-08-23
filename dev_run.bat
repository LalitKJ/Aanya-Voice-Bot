@echo off
echo Starting backend and frontend servers in Windows Terminal...

wt new-tab --title "Backend" -d "%cd%" pwsh -NoExit -Command "uv run main.py" ^
; new-tab --title "Frontend" -d "%cd%\frontend" pwsh -NoExit -Command "yarn run dev"
echo Backend and frontend servers started.