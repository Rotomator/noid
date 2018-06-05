@ECHO OFF


CHOICE /C YN /M "This will copy all files from repository, Are you sure"
IF ERRORLEVEL == 2 GOTO __end

CHOICE /C YN /M "This will overwrite all your local files, are you really sure"
IF ERRORLEVEL == 2 GOTO __end


ECHO Creating backup (in C:\_noid_dev_old)...
ECHO ===============================================================================

@ROBOCOPY /mir /nfl /ndl C:\_noid_dev C:\_noid_dev_old /XF *.pyc /XD C:\_noid_dev\_noid\submitFiles


ECHO Pulling from repository...
ECHO ===============================================================================

C:
CD C:\_noid_dev

git reset --hard noid/master
git clean -fxd
git pull noid master


:__end
@ECHO ON
@EXIT /B 0