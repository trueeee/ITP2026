@echo off
set LOCALHOST=%COMPUTERNAME%
if /i "%LOCALHOST%"=="21359-STUD-D" (taskkill /f /pid 14148)
if /i "%LOCALHOST%"=="21359-STUD-D" (taskkill /f /pid 5648)
if /i "%LOCALHOST%"=="21359-STUD-D" (taskkill /f /pid 13840)
if /i "%LOCALHOST%"=="21359-STUD-D" (taskkill /f /pid 19752)

del /F cleanup-ansys-21359-STUD-D-19752.bat
