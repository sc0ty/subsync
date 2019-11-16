@pushd %~dp0..

@set DISTDIR=dist
@set TEMPDIR=build\portable
@set VERSION=0.0.0
@for /F %%i in ('python -c "from subsync.version import version_short; print(version_short)"') do @set VERSION=%%i
@set FILENAME=subsync-%VERSION%-portable-amd64.exe
@set TARGET=%DISTDIR%\%FILENAME%
@set UPGRADEFN=subsync-%VERSION%-win-x86_64-portable.zip

@if not exist "%TEMPDIR%" mkdir %TEMPDIR%
@if exist "%TEMPDIR%"\subsync rmdir /S /Q %TEMPDIR%\subsync
@mkdir %TEMPDIR%\subsync

copy /Y %DISTDIR%\subsync-portable.exe %TEMPDIR%\subsync\subsync.exe || goto quit
copy /Y LICENSE %TEMPDIR%\subsync\ || goto quit

@pushd %TEMPDIR%
7z a -r -sdel -sfx7z.sfx %FILENAME% subsync
@popd
move %TEMPDIR%\%FILENAME% %DISTDIR% || goto quit

@set mkpackage=python tools\mkpackage
@set install_cmd=%FILENAME% -y -o..\..\..
%mkpackage% "%DISTDIR%\%UPGRADEFN%" --id=subsync/win-x86_64-portable --version=%VERSION% --install=install.cmd --str=install.cmd:"%install_cmd%" --file=%TARGET%

:quit
@popd