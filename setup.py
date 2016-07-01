# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt5app.py is a very simple type of PyQt5 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable
# import os
# os.environ['TCL_LIBRARY'] = "C:\\Users\\lidingke\\Anaconda3\\tcl\\tcl8.6"

# os.environ['TK_LIBRARY'] = "C:\\Users\\lidingke\\Anaconda3\\tcl\\tk8.6"

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        # 'includes': 'atexit',
        # 'packages': ['serial'],
        # 'include_files': ['UI'],
        'excludes':["tkinter",'PyQt4']
    }
}

executables = [
    Executable('main.py', base=base)
]

setup(name='MAP200',
      version='0.1',
      description='lidingke@yofc.com',
      options=options,
      executables=executables
      )
