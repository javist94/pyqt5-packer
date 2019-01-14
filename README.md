# pyqt5-packer
Python script which generates the necessary files to run a QT user interface using python and corrects the output from pyqt5 tool so that it doesn't have errors. Optimised for the Raspberry Pi but works well on any linux system.

Requisites: pyqt5 package. Note that you will need the qt5 runtime installed on your target machine in order for the output files to be run.

Instructions: type python3 pack.py --help for details. You can set the working directory (where your QT project is, say 'qtproj') by passing a parameter like this: python3 pack.py --dir /home/user/qtproj

The easiest way of using this script is just by placing it into the working directory and not specifying arguments. Just place it there, and type "python3 pack.py". The output will be generated in a new directory called "build".
