@CALL %NOID_PATH%\env\_env_common
@IF ERRORLEVEL 1 GOTO __error


@ECHO OFF
ECHO Setting MAYA environment variables...
ECHO ===============================================================================


REM required variables
REM ----------------------------------------------------------------
IF "%MAYA_VERSION%" == "" (
	ECHO ERROR : MAYA_VERSION not defined.
	GOTO __error
)

IF "%ARCHIVE_VERSION%" == "" (
	ECHO ERROR : ARCHIVE_VERSION not defined.
	GOTO __error
)

IF "%VRAY_VERSION%" == "" (
	ECHO ERROR : VRAY_VERSION not defined.
	GOTO __error
)


REM maya
REM ----------------------------------------------------------------
CALL %varAdd% PYTHONPATH					%NOID_PATH%\maya
CALL %varSet% MAYA_MODULE_PATH				%NOID_PATH%\maya\modules
CALL %varSet% MAYA_SHELF_PATH				%NOID_PATH%\maya\shelves
CALL %varSet% MAYA_ENABLE_LEGACY_VIEWPORT	1


REM royalrender
REM ----------------------------------------------------------------
CALL %varSet% RR_ROOT			\\storb\diskb\RoyalRender
CALL %varAdd% MAYA_PLUG_IN_PATH	%NOID_PATH%\maya\royalrender


REM vray
REM ----------------------------------------------------------------
CALL %varSet% VRAY_FOR_MAYA_ROOT						%NOID_BIN_PATH%\vray\%VRAY_VERSION%\maya%MAYA_VERSION%\maya_root
CALL %varSet% VRAY_FOR_MAYA_MAIN						%NOID_BIN_PATH%\vray\%VRAY_VERSION%\maya%MAYA_VERSION%\maya_vray

CALL %varAdd% PATH										%VRAY_FOR_MAYA_ROOT%\bin

CALL %varAdd% PYTHONPATH								%VRAY_FOR_MAYA_MAIN%\scripts
CALL %varAdd% VRAY_FOR_MAYA%MAYA_VERSION%_MAIN_x64		%VRAY_FOR_MAYA_MAIN%
CALL %varAdd% VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64	%VRAY_FOR_MAYA_MAIN%\vrayplugins
CALL %varAdd% VRAY_OSL_PATH_MAYA%MAYA_VERSION%_x64		%VRAY_FOR_MAYA_MAIN%\vrayplugins
CALL %varAdd% VRAY_AUTH_CLIENT_FILE_PATH				%NOID_BIN_PATH%\vray
CALL %varAdd% MAYA_PLUG_IN_PATH							%VRAY_FOR_MAYA_MAIN%\plug-ins
CALL %varAdd% MAYA_SCRIPT_PATH							%VRAY_FOR_MAYA_MAIN%\scripts
CALL %varAdd% XBMLANGPATH								%VRAY_FOR_MAYA_MAIN%\icons
CALL %varAdd% MAYA_RENDER_DESC_PATH						%VRAY_FOR_MAYA_ROOT%\bin\rendererDesc

"%VRAY_FOR_MAYA_MAIN%\bin\setvrlservice.exe" -server=rr


REM archives
REM ----------------------------------------------------------------
CALL %varSet% ARCHIVE_PATH								%NOID_PATH%\archive\%ARCHIVE_VERSION%

CALL %varAdd% MAYA_PLUG_IN_PATH							%ARCHIVE_PATH%\maya\plug-ins\%MAYA_VERSION%
CALL %varAdd% MAYA_SCRIPT_PATH							%ARCHIVE_PATH%\maya\scripts
CALL %varAdd% XBMLANGPATH								%ARCHIVE_PATH%\maya\icons

CALL %varAdd% VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64	%ARCHIVE_PATH%\vray\%VRAY_VERSION%


REM misc
REM ----------------------------------------------------------------
CALL %varAdd% MAYA_SCRIPT_PATH	%NOID_PATH%\maya\tools
CALL %varAdd% PYTHONPATH		%NOID_PATH%\maya\tools

CALL %varAdd% MAYA_SCRIPT_PATH	%NOID_PATH%\maya\tools\cometScripts
CALL %varAdd% MAYA_PLUG_IN_PATH	%NOID_BIN_PATH%\maya\plugins\smoothSkinClusterWeight
CALL %varAdd% MAYA_PLUG_IN_PATH	%NOID_BIN_PATH%\maya\plugins\iDeform
CALL %varAdd% MAYA_PLUG_IN_PATH	%NOID_BIN_PATH%\maya\plugins\ZivaVFX-Maya-1_2\plug-ins


@ECHO ON
@EXIT /B 0


:__error
@ECHO ON
@EXIT /B 1
