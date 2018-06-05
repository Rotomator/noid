@ECHO OFF
ECHO Setting COMMON environment variables...
ECHO -------------------------------------------------------------------------------


REM required variables
REM ----------------------------------------------------------------
IF "%NOID_PATH%" == "" (
	ECHO ERROR : NOID_PATH not defined.
	GOTO __error
)

IF "%NOID_BIN_PATH%" == "" (
	ECHO ERROR : NOID_BIN_PATH not defined.
	GOTO __error
)


SET varSet=%NOID_PATH%\env\_varSet
SET varAdd=%NOID_PATH%\env\_varAdd

CALL %varSet% PYTHONPATH %NOID_PATH%\pythonModules


@ECHO ON
@EXIT /B 0


:__error
@ECHO ON
@EXIT /B 1
