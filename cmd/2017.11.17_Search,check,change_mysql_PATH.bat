
echo %path% | find /i "mysql server 5.6" && exit 

for /f "useback delims==" %%i IN (`sc qc mysql56`) DO @echo %%i | findstr /i "mysqld">>test.txt
set /p var=<test.txt

@echo off
setlocal EnableDelayedExpansion
for /f "tokens=* delims=," %%a in (test.txt) do (
::echo %%a - input string
set x=%%a
set x=!x:"=,!
for /f "tokens=1-3 delims=," %%a in ("!x!") do echo %%b >> test1.txt
)
del test.txt

set /p var1=<test1.txt
del test1.txt
set var1=%var1:\mysqld=;%

echo %var1%

::setx /m path "%path%;%var1%"
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%path%;%var1%" /f
endlocal
exit

::del test.txt
::@echo %var%
::set var=%var:        Имя_двоичного_файла  : "=%
::@echo %var%
::set var=%var:\mysqld" --defaults-file=%
::@echo %var%