import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:/Users/ralui/AppData/Local/Programs/Python/Python36/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Users/ralui/AppData/Local/Programs/Python/Python36/tcl/tk8.6'

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = ['dill', 'python_cipres', 'string', 'subprocess', 'tempfile',
    'getopt', 'shutil', 'traceback', 'requests', 'xml', 'urllib3', 'chardet',
    'certifi', 'idna', 'pathlib', 'Bio', 'ttkthemes', 'datetime', 'tkinter'],
    excludes = ['PyQt5'],
    include_files=['C:/Users/ralui/AppData/Local/Programs/Python/Python36/DLLs/tcl86t.dll',
                   'C:/Users/ralui/AppData/Local/Programs/Python/Python36/DLLs/tk86t.dll',
                   'COPYING']
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, shortcutName='cramb',
                shortcutDir='ProgramMenuFolder', icon='cramb.ico')
]

setup(name='cramb',
      version = '2.0.5',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
