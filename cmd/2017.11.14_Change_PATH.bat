setlocal enabledelayedexpansion enableextensions

echo %path% | find /i "mysql server 5.6" && exit

set myPath="C:\Program Files\MySQL\MySQLServer 5.6\bin\mysqld.exe"
call :file_name_from_path result !myPath!
echo %result%
setx /m path "%path%;%result%;"
goto :eof

:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~dp2"
    exit /b
)

:eof

endlocal