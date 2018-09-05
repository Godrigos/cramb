#!/usr/bin/env python

"""
This file is part of cramb.

CRAMrBayesT is free software: you can redistribute it and/or modify
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

from glob import glob
from os.path import join
from download_folder_path import get_download_path as dl_dir
from get_results import get_results
from dill import load
from tkinter.messagebox import askyesno


def old_job_check():
    try:
        files = []
        for file in glob(join(dl_dir(), '*.pkl')):
            files.append(file)
        if not files:
            pass
        else:
            answer = askyesno("Pending Job Results", "It seems you have results to download from previous submissions!"
                                                     " Would you like to do it now?")
            if answer == 'yes':
                for file in files:
                    with open(join(dl_dir(), file), 'rb') as f:
                        job = load(f)
                    get_results(job)
            else:
                pass
    except IndexError:
        pass
