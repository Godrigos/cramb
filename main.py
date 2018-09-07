#!/usr/bin/env python

"""
This file is part of cramb.

cramb is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cramb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CRAMrBayesT.  If not, see <https://www.gnu.org/licenses/>.

Copyright 2018 Rodrigo Aluizio
"""

from tkinter import *
from ttkthemes import ThemedStyle
from Application import Application


root = Tk()
root.geometry('600x400')
root.resizable(width=False, height=False)
root.title("cramb - CIPRES API MrBayes Client")
style = ThemedStyle(root)
style.set_theme("vista")
Application(root)
root.iconbitmap('cramb.ico')    # Windows only
root.mainloop()
