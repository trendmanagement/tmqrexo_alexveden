This is a PyCharm 5 project with GIT repository inside, you can download Community edition of PyCharm for free
(https://www.jetbrains.com/pycharm/download/#section=windows). But PyCharm is not required for code execution,
you can run it into a browser or in command line.

HOW TO INSTALL AND RUN
----------------------

1.	Download Anaconda Python for windows (https://www.continuum.io/downloads). I’m using Python 3.4, but actual version
    is 3.5, but I think they are fully compatible.

2.	Run cmd file ‘run_notebook.cmd’, afterwards  http://localhost:8888/tree will be opened in your browser.


RUNNING CYTHON Code
-------------------
HOWTO for Python 3.5 and Anaconda v4.0

1. Install Microsoft Visual C++ Build Tools 2015. Check Windows 8.1 SDK and Windows 10 SDK options. (https://www.microsoft.com/download/details.aspx?id=49983)
2. Edit the C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat and replace its content with the following text

<-- Cut begin -->
rem Vcvarsall for Visual C++ Build Tools 2015
@echo off
set vcprogramfiles=%ProgramFiles(x86)%
if "%vcprogramfiles%"=="" set vcprogramfiles=%ProgramFiles%
call "%vcprogramfiles%\Microsoft Visual C++ Build Tools\vcbuildtools.bat" %*
<-- cut end ->>
