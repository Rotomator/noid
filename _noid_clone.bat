rem git remote set-url noid https://aganzerli:VVDokl123@github.com/aganzerli/noid.git
rem git init

@ECHO OFF

copy NUL %NOID_PATH%\time

c:
cd C:\_noid_dev

@ECHO ON
git pull noid master
git status
@ECHO OFF

choice /c:YN
IF ERRORLEVEL==2 GOTO __end

@ECHO ON
git add -A
git commit -m "commit"
@ECHO OFF

choice /c:YN
IF ERRORLEVEL==2 GOTO __end

@ECHO ON
git push noid master
@ECHO OFF

robocopy /mir %NOID_PATH% \\ad01\tools\NOID /XF *.pyc

:__end
EXIT 0