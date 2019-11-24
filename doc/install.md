# SubSync installation
You could download release builds from [download page](https://sc0ty.github.io/subsync/en/download.html).

Building SubSync is two step process. First you need to build _gizmo_ module (in folder `gizmo`), then you could build (or run under interpreter) SubSync itself.
There are several ways to build and run SubSync, it is due to significant differences in supported platforms.

## Prerequisites
For _gizmo_ module:
- C++11 compatible compiler (or better C++14);
- pybind11;
- ffmpeg libraries (4.0 or newer);
- sphinxbase and pocketsphinx.

For main module:
- Python interpreter (supporting Python 3.5 or newer);
- Python modules listed in `requirements.txt` file;
- compiled _gizmo_ module.

## Configuration
SubSync expects to find configuration in `config.py` file. You could use default from `config.py.template` and modify it if needed:
```
cp subsync/config.py.template subsync/config.py
```

## POSIX platforms
For POSIX compatibile platforms (e.g. Linux, MacOS), standard Python `setup.py` scripts are provided.

It is advised to build under Python virtual environment. To do that, go to project main directory and type:
```
pip install venv
python -m venv .env
```
You could also specify different version of Python interpreter, for details see [the docs](https://docs.python.org/3/library/venv.html).

Activate your virtual environment:
```
source .env/bin/activate
```

Build _gizmo_ module.

If you have ffmpeg, sphinxbase and pocketsphinx libraries installed and avaiable via `pkg-config`:
```
pip install ./gizmo
```

If you don't want to use `pkg-config` (or you can't), you must provide paths to these libraries manually, using evironment variables:
```
export FFMPEG_DIR=PATH
export SPHINXBASE_DIR=PATH
export POCKETSPHINX_DIR=PATH
export USE_PKG_CONFIG=no
pip install ./gizmo
```

Install main module:
```
pip install '.[GUI]'
```
If during this step wxPython fails to compile, you could try to find prebuild version for your system [here](https://extras.wxpython.org/wxPython4/extras/).

To install headless version only (without GUI):
```
pip install .
```

Run SubSync from your virtual environment:
```
./bin/subsync
```

### MacOS installer
MacOS binary distribution and installer are generated using pyinstaller utility. To build executable, with gizmo installed, type:
```
pip install pyinstaller
pyinstaller macos.spec
```

To create dmg installer, you need to have [create-dmg](https://github.com/andreyvit/create-dmg) in your path:
```
./tools/package-macos.sh
```

## Windows
Building Windows version under virtual environment is similar to building POSIX version. You need a [Python runtime](https://www.python.org/downloads/windows/), then you could setup and activate virtual environment:
```
python -m pip install venv
python -m venv .env
.env\Scripts\activate.bat
```

To build gizmo, you need to provide dependencies first.
Sphinxbase and pocketsphinx are published with Visual Studio solution file, which is [easy to use](https://github.com/cmusphinx/pocketsphinx#ms-windows-ms-visual-studio-2012-or-newer---we-test-with-vc-2012-express).
Building ffmpeg on the other hand is not that easy. You could use [official build](https://ffmpeg.zeranoe.com/builds/) instead.

Install _gizmo_ module:
```
set FFMPEG_DIR=d:\projects\ffmpeg
set SPHINXBASE_DIR=d:\projects\sphinxbase
set POCKETSPHINX_DIR=d:\projects\pocketsphinx
set USE_PKG_CONFIG=no
pip install .\gizmo
```

Install main module:
```
pip install .[GUI]
```

To install headless version only (without GUI):
```
pip install .
```

Run SubSync from your virtual environment:
```
python bin\subsync
```

### Windows installer
Windows binary distribution and installer are generated using pyinstaller utility. To build executable, with gizmo installed, type:
```
pip install pyinstaller
pyinstaller windows.spec
```

To create msi installer, you need to have [WIX Toolset](https://wixtoolset.org) in your path:
```
tools\package-windows.cmd
```

To create portable version, you need [7-Zip](https://www.7-zip.org) in your path:
```
tools\package-windows-portable.cmd
```

## Ubuntu SNAP
Technically [snaps](https://snapcraft.io) are universal linux packages, but it looks like they are really fully supported only on Ubuntu.

To build one, just type `snapcraft` in the project main directory.
Thats it, no need to prepare virtual envirnoment, installing dependencies nor building gizmo. Everything needed will be downloaded and built automatically.

## Running without installation
To simplify development, SubSync can be run without main module installation. Dependencies and _gizmo_ module still must be installed:
```
pip install ./gizmo
pip install -r requirements
python run.py
```
