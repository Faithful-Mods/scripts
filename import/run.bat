@echo off
echo ------------------------------------------------------------
echo(
echo [1/?] Applying settings...
echo(
echo ------------------------------------------------------------
echo Warning : Python is required to use this script.
echo Warning : PyGithub is required to use this script, install command : pip install PyGithub

echo(
set /p MCVersion=Minecraft version : 
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

python py\check_settings.py "%MCVersion%"

echo ------------------------------------------------------------
echo(
echo [3/?] Import files to GitHub...
echo(
echo ------------------------------------------------------------ 
echo TO USE THIS SCRIPTS, YOU NEED TO BE A MEMBER OF FAITHFUL MODS ORGANIZATION ON GITHUB : https://github.com/Faithful-Mods
echo(
set /p Username=GitHub username : 
set /p Password=GitHub password : 
echo(
python py\github_import.py "%MCVersion%" "%Username%" "%Password%"

echo ------------------------------------------------------------
echo(
echo [4/?] Add files to the mod list...
echo(
echo ------------------------------------------------------------ 

cd ..
set /p ModsPath=<user_settings/path_mods_list.txt
echo PATH MODS LIST : %ModsPath%

pause
exit