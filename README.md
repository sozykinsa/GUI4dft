GUI4dft (Graphical User Interface for support of Density Functional Theory calculations) - first free SIESTA oriented GUI. It is a cross-platform program. 

GUI4DFT program is written in Python 3 (version >= 3.4). It has some dependences. To install the necessary modules, run in the terminal (command line):

pip3 install pyqt5 numpy scipy pyopengl matplotlib scikit-image 

In Ubuntu, do extra: 

sudo apt-get install qt5-default

These commands are suitable for Windows 10, Ubuntu 20, Mas OS Majave. For other distributions and operating systems, the command and set of required packages may differ.

To run the program, type

python3 gui4dft.py

If the program was helpful in your research, please cite the article https://doi.org/10.1016/j.cpc.2021.107843