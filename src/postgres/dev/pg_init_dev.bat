@echo off
if "%OS%" == "Windows_NT" setlocal

rem ---------------------------------------------------------------------------
rem pg init bat
rem
rem
rem Environment Variable Prequisites:
rem
rem   POSTGRES_HOME   PostgresSql Installation Directory
rem
rem
rem @author yan
rem
rem $Id: pg_init.bat 1000 2023-02-27 10:16:00 yan $
rem ---------------------------------------------------------------------------

rem Guess POSTGRES_HOME if not defined
set CURRENT_DIR=%cd%
if not "%POSTGRES_HOME%" == "" goto gotHome
set POSTGRES_HOME=%CURRENT_DIR%
if exist "%POSTGRES_HOME%\bin\psql.exe" goto okHome
cd ..
set POSTGRES_HOME=%cd%
cd %CURRENT_DIR%
:gotHome
if exist "%POSTGRES_HOME%\bin\psql.exe" goto okHome
echo The POSTGRES_HOME environment variable is not defined correctly
echo %POSTGRES_HOME%\bin\psql.exe not exist
goto end
:okHome

set CURRENT_DIR=%~dp0
set DB_INIT_DIR=%CURRENT_DIR%..

set dbname=pingpong-match
set dbuser=postgres
set dbpass=postgres

set PGPASSWORD=%dbpass%
rem set PGCLIENTENCODING=UTF8

rem echo %DB_INIT_DIR%
rem echo %POSTGRES_HOME%
echo dbname = %dbname%

set inputDrop=
set /P inputDrop="Do you confirm to drop database %dbname% (*required) ? [Y|N] "
set ifDrop=0
if "%inputDrop%"=="Y" set ifDrop=1
if "%inputDrop%"=="y" set ifDrop=1
if %ifDrop% equ 1 (
  echo=
  echo * Disconnect %dbname%
  "%POSTGRES_HOME%\bin\psql.exe" -U %dbuser% -c "select pg_terminate_backend(pid) from pg_stat_activity where datname='%dbname%'";
  echo * Drop database %dbname%
  "%POSTGRES_HOME%\bin\psql.exe" -U %dbuser% -c "DROP DATABASE IF EXISTS \"%dbname%\""
) else (
  echo * Exit
  goto eof
)

echo=
echo * Creating database %dbname%, about 50 seconds ...
rem "%POSTGRES_HOME%\bin\psql.exe" -U %dbuser% -c "DO $do$ BEGIN IF EXISTS (SELECT 1 FROM pg_database WHERE datname = '%dbname%') THEN RAISE NOTICE '%dbname% exists.'; ELSE PERFORM dblink_exec('dbname=', 'CREATE DATABASE %dbname%'); END IF; END $do$"
"%POSTGRES_HOME%\bin\psql.exe" -U %dbuser% -c "CREATE DATABASE \"%dbname%\""

call:importSQLFile init_journal.sql
call:importSQLFile init_auth.sql
call:importSQLFile init_public.sql

call:importCSVFile auth group
call:importCSVFile auth user
call:importCSVFile auth user_group
call:importCSVFile auth menu
call:importCSVFile auth group_menu

call:importSQLFile id_seq_reset.sql

echo [Finished]
goto end

:importSQLFile
echo import '%DB_INIT_DIR%\%~1'
"%POSTGRES_HOME%\bin\psql.exe" -U %dbuser% -d %dbname% -f "%DB_INIT_DIR%\%~1"
goto eof

:importCSVFile
echo COPY %~1.%~2 FROM '%DB_INIT_DIR%\csv\%~1.%~2.csv'
"%POSTGRES_HOME%\bin\psql.exe" -U %dbuser% -d %dbname% -c "SET client_encoding = 'UTF8'; COPY %~1.%~2 FROM '%DB_INIT_DIR%\csv\%~1.%~2.csv' WITH CSV HEADER"
goto eof

:end
pause

:eof
