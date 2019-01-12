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

## POSIX platforms
For POSIX compatibile platforms (e.g. Linux), standard Python `setup.py` scripts are provided.

It is advised to build under Python virtualenv. To do that, go to project main directory and type:
```
pip install virtualenv
virtualenv venv
```
You could also specify different version of Python interpreter, for details see [the docs](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv).

Then activate your virtualenv and install required packages:
```
source venv/bin/activate
pip install -r requirements.txt
```
If during this step, wxPython fails to compile, you could try to find prebuild version for your system [here](https://extras.wxpython.org/wxPython4/extras/).

If you have ffmpeg, sphinxbase and pocketsphinx libraries installed and avaiable via `pkg-config`, you could now build _gizmo_:
```
cd gizmo
python setup.py build
```

If you don't want to use `pkg-config` (or you can't), you must provide paths to these libraries manually using following options:
```
--ffmpeg-dir=PATH
--sphinxbase-dir=PATH
--pocketsphinx-dir=PATH
--use-pkg-config=yes|no
```
Or env variables:
```
FFMPEG_DIR=PATH
SPHINXBASE_DIR=PATH
POCKETSPHINX_DIR=PATH
USE_PKG_CONFIG=yes|no
```

And then install it under virtualenv, e.g.:
```
export FFMPEG_DIR=~/projects/ffmpeg
export SPHINXBASE_DIR=~/projects/sphinxbase
export POCKETSPHINX_DIR=~/projects/pocketsphinx
export USE_PKG_CONFIG=no
python setup.py build
python setup.py install
```

Now you could run SubSync from your virtualenv
```
python subsync.py
```

## Windows
Building Windows version under virtualenv is similar to building POSIX version. You need a [Python runtime](https://www.python.org/downloads/windows/), then you could setup and activate environment:
```
python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To build gizmo, you need to provide dependencies first.
Sphinxbase and pocketsphinx are published with Visual Studio solution file, which is [easy to use](https://github.com/cmusphinx/pocketsphinx#ms-windows-ms-visual-studio-2012-or-newer---we-test-with-vc-2012-express).
Building ffmpeg on the other hand is not that easy. You could use [official build](https://ffmpeg.zeranoe.com/builds/) instead.

With everythong prepared, gizmo can be installed now under virtualenv:
```
cd gizmo
set FFMPEG_DIR=d:\projects\ffmpeg
set SPHINXBASE_DIR=d:\projects\sphinxbase
set POCKETSPHINX_DIR=d:\projects\pocketsphinx
set USE_PKG_CONFIG=no
python setup.py build
python setup.py install
```

And SubSync is ready to be run:
```
python subsync.py
```

### Windows installer
Windows binary distribution and installer are generated using cx-Freeze utility. To build executable, with gizmo installed, type:
```
python setup.py build_exe
```
And to create msi installer:
```
python setup.py bdist_msi
```
For more information, please refer to the [cx-Freeze docs](https://cx-freeze.readthedocs.io/en/latest/).

## Ubuntu SNAP
Technically [snaps](https://snapcraft.io) are universal linux packages, but it looks like they are really fully supported on Ubuntu.

To build one, just type `snapcraft` in the project main directory.
Thats it, no need to prepare virtualenv, installing dependencies nor building gizmo. Everything needed will be downloaded and built automatically.
