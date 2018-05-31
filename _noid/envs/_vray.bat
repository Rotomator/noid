IF DEFINED %MAYA_VERSION% () ELSE (
	@ECHO ERROR : MAYA_VERSION not defined.
	@EXIT /B 0
)

IF DEFINED %ARCHIVE_VERSION% () ELSE (
	@ECHO ERROR : ARCHIVE_VERSION not defined.
	@EXIT /B 0
)

IF DEFINED %VRAY_VERSION% () ELSE (
	@ECHO ERROR : VRAY_VERSION not defined.
	@EXIT /B 0
)


@ECHO OFF


REM maya
REM ----------------------------------------------------------------
CALL _varSet MAYA_ENABLE_LEGACY_VIEWPORT 1


REM archives
REM ----------------------------------------------------------------
CALL _varSet ARCHIVE_PATH %NOID_PATH%\archive\%ARCHIVE_VERSION%


REM vray
REM ----------------------------------------------------------------
CALL _varSet VRAY_FOR_MAYA_MAIN		%NOID_BIN_PATH%\vray\%VRAY_VERSION%\maya%MAYA_VERSION%\maya_vray
CALL _varSet VRAY_FOR_MAYA_ROOT		%NOID_BIN_PATH%\vray\%VRAY_VERSION%\maya%MAYA_VERSION%\maya_root
CALL _varSet VRAY_FOR_MAYA_PLUGINS	%VRAY_FOR_MAYA_MAIN%\vrayplugins

CALL _varAdd PATH										%VRAY_FOR_MAYA_ROOT%\bin
CALL _varAdd VRAY_FOR_MAYA%MAYA_VERSION%_MAIN_x64		%VRAY_FOR_MAYA_MAIN%
CALL _varAdd VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64	%VRAY_FOR_MAYA_PLUGINS%
CALL _varAdd VRAY_OSL_PATH_MAYA%MAYA_VERSION%_x64		%VRAY_FOR_MAYA_PLUGINS%
CALL _varAdd VRAY_AUTH_CLIENT_FILE_PATH					%NOID_BIN_PATH%\vray
CALL _varAdd MAYA_PLUG_IN_PATH							%VRAY_FOR_MAYA_MAIN%\plug-ins
CALL _varAdd MAYA_SCRIPT_PATH							%VRAY_FOR_MAYA_MAIN%\scripts
CALL _varAdd XBMLANGPATH								%VRAY_FOR_MAYA_MAIN%\icons


REM royalrender
REM ----------------------------------------------------------------
CALL _varSet RR_ROOT			\\storb\diskb\RoyalRender
CALL _varAdd MAYA_PLUG_IN_PATH	%NOID_PATH%\maya\royalrender


REM misc
REM ----------------------------------------------------------------
CALL _varAdd MAYA_SCRIPT_PATH	%NOID_PATH%\maya\tools
CALL _varAdd MAYA_SCRIPT_PATH	%NOID_PATH%\maya\tools\cometScripts
CALL _varAdd MAYA_PLUG_IN_PATH	%NOID_BIN_PATH%\maya\plugins\smoothSkinClusterWeight
CALL _varAdd MAYA_PLUG_IN_PATH	%NOID_BIN_PATH%\maya\plugins\iDeform
CALL _varAdd MAYA_PLUG_IN_PATH	%NOID_BIN_PATH%\maya\plugins\ZivaVFX-Maya-1_2\plug-ins


@ECHO ON