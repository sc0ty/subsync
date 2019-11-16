@pushd %~dp0..

@set DISTDIR=dist
@set TEMPDIR=build\installer
@set UPGRADEDIR=%TEMPDIR%\upgrade
@set RESDIR=resources
@set VERSION=0.0.0
@for /F %%i in ('python -c "from subsync.version import version_short; print(version_short)"') do @set VERSION=%%i
@set FILENAME=subsync-%VERSION%-amd64.msi
@set UPGRADEFN=subsync-%VERSION%-win-x86_64.zip
@set TARGET=%DISTDIR%\%FILENAME%

@if not exist "%TEMPDIR%" mkdir %TEMPDIR%
heat dir %DISTDIR%\subsync -cg Files -dr INSTALLDIR -var var.SourceDir -gg -sfrag -suid -srd -sw5150 -nologo -template fragment -out %TEMPDIR%\directory.wxs || goto quit
candle -nologo -arch x64 -dVersion=%VERSION% -out %TEMPDIR%\subsync.wixobj %RESDIR%\subsync.wxs || goto quit
candle -nologo -arch x64 -out %TEMPDIR%\wixui.wixobj %RESDIR%\wixui.wxs || goto quit
candle -nologo -arch x64 -dSourceDir=%DISTDIR%\subsync -out %TEMPDIR%\directory.wixobj %TEMPDIR%\directory.wxs || goto quit
light -nologo -ext WixUIExtension -ext WixUtilExtension -cultures:en-us -out %TARGET% %TEMPDIR%\subsync.wixobj %TEMPDIR%\directory.wixobj %TEMPDIR%\wixui.wixobj || goto quit

@set mkpackage=python tools\mkpackage
@set install_cmd=start msiexec.exe /i %FILENAME%
%mkpackage% "%DISTDIR%\%UPGRADEFN%" --id=subsync/win-x86_64 --version=%VERSION% --install=install.cmd --str=install.cmd:"%install_cmd%" --file=%TARGET%

:quit
@popd