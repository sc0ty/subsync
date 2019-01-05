# SubSync architecture overview
SubSync is composed of two main modules:
- main module written in Python;
- _gizmo_ written in C++ and compiled to Python binary module.

Main module is responsible for displaying GUI, asset downloading and installation and contains business logic, whereas gizmo is doing heavy lifting such as speech recognition, audio and subtitle extraction and synchronization.

## Main module
Written in Python (3.5 or never).

## Gizmo
Written in C++11 with [pybind11](https://github.com/pybind/pybind11), compiled as Python binary module. Uses [ffmpeg](https://ffmpeg.org) libraries for media extraction and [pocketsphinx](https://cmusphinx.github.io) for speech recognition.
