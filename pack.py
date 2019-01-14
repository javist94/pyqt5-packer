#!bin/env bash
#
# Title: pyqt5-packer (pyqtpack)
# Author: Javier Gallardo
# Date: Jan 2019
#
#

import subprocess
import os
from pathlib import Path
import argparse

#Global vars definition
rawfilename = "mainwindow_auto_raw.py"
finalfilename = "mainwindow_auto"
packhelperFileName = "pack_helper.sh"
output_dir = "build"
input_filename = "mainwindow.ui"
working_path = os.getcwd();

#Embedded file

py_mainfile_header = """ # always seem to need this
import sys
 
# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *
 
# This is our window from QtCreator
import """

py_mainfile_tail = """
 
# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
 # access variables inside of the UI's file
 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self) # gets defined in the UI file
 
# I feel better having one of these
def main():
 # a new app instance
 app = QApplication(sys.argv)
 form = MainWindow()
 form.showFullScreen()
 # without this, the script exits immediately.
 sys.exit(app.exec_())
 
# python bit to figure how who started This
if __name__ == '__main__':
 main()"""


#Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Project directory. Assumed to be in the same path as this script if not specified. No final slash, please.")
parser.add_argument("-d", "--dir", help="Output folder name. This is '" + output_dir + "' by default. Will be created if it doesn't exist.")
parser.add_argument("-i", "--inputfn", help="Input filename. Assumed to be '" + input_filename + "' if not specified.")
parser.add_argument("-o", "--outputfn", help="Output filename (without file extension) for the window QT class definition. This is 'mainwindow_auto' by default.")
parser.add_argument("-m", "--mainfile", help="Generate a template to start. 'main.py' will be generated.", action="store_true")
args = parser.parse_args()

if args.path is not None:
	working_path = args.path
if args.dir is not None:
	output_dir = args.dir
if args.inputfn is not None:
	input_filename = args.inputfn

#We check that subdir "build" exists, if not, we create it
if not os.path.isdir(working_path + "/" + output_dir):
	print("> No output directory named " + "'" + output_dir + "'" + " present.")
	os.mkdir(working_path + "/" + output_dir, 0o755)
	print("> Directory created.")

ph_file_check = Path(working_path + "/" + packhelperFileName)
if ph_file_check.is_file():
	os.remove(working_path + "/" + packhelperFileName)

print("> Creating a clean, working version of pyqt5 tool output.")
phfile = open(working_path + "/" + packhelperFileName, "w")
phfile.write("pyuic5 " + input_filename + " > " + rawfilename)
phfile.close()

sp1 = subprocess.Popen(["bash", working_path + "/" + packhelperFileName])
sp1.wait()

os.remove(working_path + "/" + packhelperFileName)

raw_qtuifile = open(working_path + "/" + rawfilename, "r")

clean_qtfilecontents = ""; removed_lines = 0;
for line in raw_qtuifile:
	if "QtGui.QPalette.PlaceholderText" not in line:
		clean_qtfilecontents = clean_qtfilecontents + line
	else:
		removed_lines = removed_lines + 1

raw_qtuifile.close();
os.remove(working_path + "/" + rawfilename)
print("> Done. Removing temp files.")

target_file = Path(working_path + "/" + output_dir + "/" + finalfilename + ".py")
if target_file.is_file():
	os.remove(working_path + "/" + output_dir + "/" + finalfilename + ".py")
	print("> A previous version of the target file already exists. Will be replaced.")

new_qtuifile = open(working_path + "/" + output_dir + "/" + finalfilename + ".py", "w")
new_qtuifile.write(clean_qtfilecontents)
new_qtuifile.close()
print("> Done.")

if args.mainfile:
	print("> Writing main.py file")
	if os.path.isfile(working_path + "/" + output_dir + "/main.py"):
		print("> main.py already exists. Will be replaced.")
		os.remove(working_path + "/" + output_dir + "/main.py")
	mainpyfile = open(working_path + "/" + output_dir + "/main.py", "w")
	mainpyfile.write(py_mainfile_header + finalfilename + py_mainfile_tail)
	mainpyfile.close()
	print("> Done.")


print("> This program has successfully finished.")