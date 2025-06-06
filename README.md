<a href="https://codecov.io/gh/sozykinsa/GUI4dft">
  <img src="https://codecov.io/gh/sozykinsa/GUI4dft/branch/master/graph/badge.svg?token=DFP49S1OVG"/>
</a>

GUI4dft (Graphical User Interface for support of Density Functional Theory calculations) - first free SIESTA oriented GUI. It is a cross-platform program. 

## Install
GUI4DFT program is written in Python 3 (version 3.9, 3.10 or 3.11). It has some dependences. To install the necessary modules, run in the terminal (in the <gui4dft path>):

pip3 install -r ./requirements.txt

To run the program, type (in the <gui4dft path>/src)

python3 gui4dft.py

## Problems with Install?

You have to set the variable QT_API:

export QT_API=pyside6 (in linux) and QT_API=pyqt5 (in Windows)

Some operating systems may require additional packages to be installed:

Ubuntu 22.04: sudo apt-get install -y libxcb-cursor-dev


## Explanations for the versions of the program

v1.0 - The version of the program described in the article https://doi.org/10.1016/j.cpc.2021.107843

v1.1 - Minor changes compared to version v1.0. Mostly bugs fixed.

v1.2 - Contains some additional features. For example, it allows visualizing the critical paths of connections (critic2), preparing scripts for calculating spectra using PyNao. The 1.x versions of GUI4dft do not have hard-to-install dependencies and are easy to run on most popular operating systems.

v1.3 - This version uses pyqtgraph instead of matplotlib and pyside2 instead of PyQt5. The colors of the atoms and covalent radii are taken from the ASE module. The project is covered with tests.

v1.4 - Pyside6. Added support for exporting structural data to input files VASP, CRYSTAL, QE. 

v1.5 - This is the next release. Pyside6 for Linux and PyQt5 for Windows.

The master branch contains more or less stable 1.x version functions.

## Code testing
Automatic code testing (pytest, except OpenGL code) is performed on GitHub (Ubuntu, Windows and Mac). Manual and pytest (with OpenGL code) testing is performed in Ubuntu and Windows.

## Authors and acknowledgment
If the program was helpful in your research, please cite the article https://doi.org/10.1016/j.cpc.2021.107843