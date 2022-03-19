<a href="https://codecov.io/gh/sozykinsa/GUI4dft">
  <img src="https://codecov.io/gh/sozykinsa/GUI4dft/branch/master/graph/badge.svg?token=DFP49S1OVG"/>
</a>

GUI4dft (Graphical User Interface for support of Density Functional Theory calculations) - first free SIESTA oriented GUI. It is a cross-platform program. 

## Install
GUI4DFT program is written in Python 3 (version >= 3.4). It has some dependences. To install the necessary modules, run in the terminal (command line):

pip3 install pyside2 numpy scipy pyopengl pyqtgraph matplotlib scikit-image

These commands are suitable for Windows 10, Ubuntu 20, Mas OS Majave. For other distributions and operating systems, the command and set of required packages may differ.

You have to set the variable QT_API:

export QT_API=pyside2 (in linux, or https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/ in Windows)

To run the program, type

python3 gui4dft.py

## Explanations for the versions of the program

v1.0 - The version of the program described in the article https://doi.org/10.1016/j.cpc.2021.107843

v1.1 - Minor changes compared to version v1.0. Mostly bugs fixed.

v1.2 - Contains some additional features. For example, it allows visualizing the critical paths of connections (critic2), preparing scripts for calculating spectra using PyNao. The 1.x versions of GUI4dft do not have hard-to-install dependencies and are easy to run on most popular operating systems.

v1.3 - This is the next release in 1.x branch. This version will use pyqtgraph instead of matplotlib and pyside2 instead of PyQt5.

The master branch contains more or less stable 1.x version functions.

## Code testing
Automatic code testing (pytest, except OpenGL code) is performed on GitHub (Ubuntu, Windows and Mac). Manual and pytest (with OpenGL code) testing is performed in Ubuntu and Windows.

## Authors and acknowledgment
If the program was helpful in your research, please cite the article https://doi.org/10.1016/j.cpc.2021.107843