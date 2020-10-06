@echo off
echo ------------------------------------------------------------
echo(
echo [1/?] Applying settings...
echo(
echo ------------------------------------------------------------

cd ..
set /p ModsPath=<user_settings/path_mods_list.txt
echo PATH MODS LIST : %ModsPath%

cd import

echo(
set /p MCVersion=Which version did you want to import ? 
echo(
set /p Choice=Have you placed mods resource pack under the /mods folder [Y/N]? 
echo(

if not '%Choice%'=='' set Choice=%Choice:~0,1%
if '%Choice%'=='Y' goto yes
if '%Choice%'=='y' goto yes
if '%Choice%'=='N' goto no
if '%Choice%'=='n' goto no
if '%Choice%'=='' goto no
echo "%Choice%" is not valid
echo.
goto start

:no
echo You need to place all your mods resource in the /resources folder following this : "/resources/<asset_name>/..."
echo ex: "/resources/minecraft/..." or ex: "/resources/botania/..."
pause
exit

:yes
echo ------------------------------------------------------------
echo(
echo [2/?] Check settings...
echo(
echo ------------------------------------------------------------ 

python py\import.py "%MCVersion%"

echo ------------------------------------------------------------
echo(
echo [3/?] Import files to GitHub...
echo(
echo ------------------------------------------------------------ 

python py\github.py "%MCVersion%"

pause
exit