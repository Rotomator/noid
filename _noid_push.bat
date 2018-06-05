rem git remote set-url noid https://aganzerli:VVDokl123@github.com/aganzerli/noid.git
rem git init

@ECHO OFF


ECHO Syncing with repository...
ECHO ===============================================================================


C:
CD C:\_noid_dev

git pull noid master
git status

CHOICE /C YN
IF ERRORLEVEL==2 GOTO __end


git add -A
git commit -m "commit"

CHOICE /C YN
IF ERRORLEVEL==2 GOTO __end


git push noid master


COPY NUL %NOID_PATH%\time
robocopy /mir /nfl /ndl %NOID_PATH% \\ad01\tools\NOID /XF *.pyc /XD submitFiles


PAUSE


:__end
@ECHO ON
@EXIT /B 0