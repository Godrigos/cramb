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
from tkinter.ttk import *
from os import makedirs, remove
from os.path import exists, join
from requests.exceptions import ConnectionError
from download_folder_path import get_download_path as dl_dir
from tkinter import messagebox
import python_cipres.client as cra


def get_results(self, job):
    """
    While loop that evaluates Job status and download the result
    when the job is complete.
    """
    self.send_button.config(state=DISABLED)
    self.mb_font = Style()
    self.mb_font.configure('TMessageBox', font=('Helvetica', 8))
    while True:
        try:
            job.update().wait(600)
            while not job.isDone():
                try:
                    job.update()
                    self.text_box.config(state=NORMAL)
                    self.text_box.insert(END, job.messages[-1] + '\n', "cool")
                    self.text_box.config(state=DISABLED)
                except ConnectionError:
                    self.text_box(state=NORMAL)
                    self.text_box.insert(END, "Connection lost! Will keep trying!\n", "error")
                    self.text_box(state=DISABLED)
                    pass
            else:
                # Create a directory to store the results
                dld = join(dl_dir(), str(job.metadata['clientJobName']))

                if not exists(dld):
                    makedirs(dld)

                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "Downloading results of " + str(job.metadata['clientJobName']) + '.\n',
                                     "cool")
                self.text_box.config(state=DISABLED)

                result_files = job.listResults(final=True)

                try:
                    j = 0
                    for filename in result_files:
                        result_files[filename].download(directory=dld)
                        j += 1
                        self.progress.config(value=j, maximum=len(result_files)-1)
                        self.progress.update()
                except ConnectionError:
                    self.text_box.config(state=NORMAL)
                    self.text_box.insert(END, "Connection lost!\nRestart the application and confirm the download of"
                                              "previous results", "error")
                    self.text_box.config(state=DISABLED)
                    self.send_button.config(state=NORMAL)

                job.delete()
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "Job completed and files downloaded!\n", "cool")
                self.text_box.config(state=DISABLED)
                remove(join(dl_dir(), str(job.metadata['clientJobName'] + '.pkl')))
                self.send_button.config(state=NORMAL)
        except SystemExit:
            confirm = messagebox.askyesno("Job executing!", "Are you sure you want to exit?", justify=CENTER)
            if confirm:
                messagebox.showwarning("Job result pending!", "You current job results will not be downloaded "
                                                              "automatically you will have to retrieve the results "
                                                              "later! Restart this application and confirm the "
                                                              "download of results from previous submissions!",
                                       icon='warning', justify=CENTER)
                self.send_button.config(state=NORMAL)
                quit()
            else:
                continue
        except cra.CipresError:
            self.send_button.config(state=NORMAL)
            break
