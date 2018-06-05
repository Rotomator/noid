CALL %NOID_PATH%\env\_env_common
@IF ERRORLEVEL 1 GOTO __error


@ECHO OFF
ECHO Setting NUKE environment variables...
ECHO -------------------------------------------------------------------------------


REM royalrender
REM ----------------------------------------------------------------
CALL %varSet% RR_ROOT \\storb\diskb\RoyalRender


REM nuke
REM ----------------------------------------------------------------
CALL %varAdd% NUKE_PATH %NOID_PATH%\nuke
CALL %varAdd% NUKE_PATH %NOID_BIN_PATH%\nuke
CALL %varAdd% NUKE_PATH %NOID_BIN_PATH%\nuke\LensDistort\Nuke10.5
CALL %varAdd% NUKE_PATH %NOID_PATH%\nuke\gizmos


@ECHO ON
@EXIT /B 0


:__error
@ECHO ON
@EXIT /B 1
