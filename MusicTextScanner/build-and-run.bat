@echo off
echo Building Music Text Scanner...
mvn clean package
if %errorlevel% neq 0 (
  echo Build failed. Make sure Java 17+ and Maven are installed.
  pause
  exit /b %errorlevel%
)
echo Starting app...
java -jar target\MusicTextScanner-1.0.0.jar
pause
