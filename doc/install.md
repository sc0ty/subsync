# SubSync installation
You could download release builds from [download page](https://sc0ty.github.io/subsync/en/download.html).

## Prerequisites
- C++11 compatible compiler (or better C++14);
- pybind11;
- ffmpeg libraries (4.0 or newer);
- pocketsphinx;
- Python interpreter (supporting Python 3.5 or newer);
- Python modules listed in `requirements.txt` file;

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

If you have ffmpeg and pocketsphinx libraries installed and avaiable via `pkg-config`, it will be configured automatically. Otherwise, you must provide paths to these libraries manually, using evironment variables:
```
export FFMPEG_DIR=PATH
export POCKETSPHINX_DIR=PATH
export USE_PKG_CONFIG=no
```

Install GUI version:
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
MacOS binary distribution and installer are generated using pyinstaller utility.
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

To build subsync, you need to provide dependencies first.
pocketsphinx is published with a Visual Studio solution file, which is [easy to use](https://github.com/cmusphinx/pocketsphinx#ms-windows-ms-visual-studio-2012-or-newer---we-test-with-vc-2012-express).
Building ffmpeg on the other hand is not that easy. You could use [official build](https://ffmpeg.zeranoe.com/builds/) instead.

Configure dependencies paths:
```
set FFMPEG_DIR=d:\projects\ffmpeg
set POCKETSPHINX_DIR=d:\projects\pocketsphinx
set USE_PKG_CONFIG=no
```

Install GUI version:
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
Windows binary distribution and installer are generated using pyinstaller utility.
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
Thats it, no need to prepare virtual envirnoment, installing dependencies etc. Everything needed will be downloaded and built automatically.

If process fails with message `ERROR: Failed building wheel for subsync`, try this workaround before `snapcraft`:
```
echo "[build_ext]" >> setup.cfg
echo "include_dirs=$PWD/stage/include/python3.5m" >> setup.cfg
```

## Running without installation
To simplify development, SubSync can be run without main module installation.
```
pip install -r requirements
python setup.py install
python run.py
```
