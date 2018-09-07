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
from tkinter.filedialog import askopenfilename
from tkinter.font import nametofont
from pathlib import Path
from Bio import AlignIO
from Bio.Nexus.Nexus import NexusError
from os.path import splitext, basename, join
import python_cipres.client as cra
from requests.exceptions import ConnectionError
from download_folder_path import get_download_path as dl_dir
from dill import dump, load
from get_results import get_results
from job_show import job_show
from glob import glob


class Application:
    def __init__(self, master=None):
        self.home_dir = str(Path.home())
        self.url_val = IntVar(value=0)
        self.validate = False
        self.valid_val = IntVar(value=0)
        self.conf = self.getconfig()
        self.file_path = StringVar(value="File path")

        self.default_font = nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=10)
        self.cb_font = Style()
        self.cb_font.configure('TCheckbutton', font=('Helvetica', 8))
        self.mb_font = Style()
        self.mb_font.configure('TMessageBox', font=('Helvetica', 8))

        self.file_label = Label(master, text="File:", font=('Helvetica', 10, 'bold'))
        self.file_label.place(relx=0.04, rely=0.015, height=25)

        self.choose_file = Entry(master, textvariable=self.file_path, width=60, state=DISABLED, font=('Helvetica', 10))
        self.choose_file.place(relx=0.093, rely=0.015, height=25)

        self.select_button = Button(master, text="Select File", command=self.getfile)
        self.select_button.place(relx=0.82, rely=0.015, height=25)

        self.login_lab = Label(master, text="Login Information", font=('Helvetica', 10, 'bold'), anchor=CENTER)
        self.login_lab.place(relx=0, rely=0.088, width=600, height=20)

        self.user_lab = Label(master, text='User:', font=('Helvetica', 8))
        self.user_lab.place(relx=0.005, rely=0.16, height=20)
        self.user = Entry(master, width=20, font=('Helvetica', 8))
        self.user.insert(0, self.conf['USERNAME'])
        self.user.place(relx=0.056, rely=0.16, height=20)

        self.passwd_lab = Label(master, text='Password:', font=('Helvetica', 8))
        self.passwd_lab.place(relx=0.005, rely=0.23, height=20)
        self.passwd = Entry(master, width=15, font=('Helvetica', 8), show='*')
        self.passwd.insert(0, self.conf['PASSWORD'])
        self.passwd.place(relx=0.106, rely=0.23, height=20)

        self.appname_lab = Label(master, text='App Name:', font=('Helvetica', 8))
        self.appname_lab.place(relx=0.29, rely=0.16, height=20)
        self.appname = Entry(master, width=20, font=('Helvetica', 8))
        self.appname.insert(0, self.conf['APPNAME'])
        self.appname.place(relx=0.39, rely=0.16, height=20)

        self.appid_lab = Label(master, text='App ID:', font=('Helvetica', 8))
        self.appid_lab.place(relx=0.29, rely=0.23, height=20)
        self.appid = Entry(master, width=23, font=('Helvetica', 8))
        self.appid.insert(0, self.conf['APPID'])
        self.appid.place(relx=0.36, rely=0.23, height=20)

        self.server_url_lab = Label(master, text='URL:', font=('Helvetica', 8))
        self.server_url_lab.place(relx=0.63, rely=0.23, height=20)
        self.server_url = Entry(master, width=30, font=('Helvetica', 8))
        self.server_url.insert(0, self.conf['URL'])
        self.server_url.config(state=DISABLED)
        self.server_url.place(relx=0.68, rely=0.23, height=20)

        self.url_state = Checkbutton(master, text='Modify Server URL', variable=self.url_val,
                                     command=self.url_radio)
        self.url_state.place(relx=0.73, rely=0.165)

        self.valid = Checkbutton(master, text='Validate only', variable=self.valid_val,
                                 command=self.valid_radio)
        self.valid.place(relx=0.23, rely=0.93)

        self.text_box = Text(master, state=DISABLED, font=('Consolas', 8))
        self.text_box.place(relx=0.005, rely=0.3, width=575, height=220)

        self.scrollb = Scrollbar(master, orient=VERTICAL, command=self.text_box.yview)
        self.scrollb.place(relx=0.965, rely=0.3, width=20, height=220)

        self.text_box.config(yscrollcommand=self.scrollb.set)

        self.progress = Progressbar(master, orient="horizontal", mode="determinate")
        self.progress.place(relx=0.005, rely=0.86, width=593, height=20)

        self.send_button = Button(master, text="Submit", command=self.mb_submit)
        self.send_button.place(relx=0.079, rely=0.92, height=25)

        self.close_button = Button(master, text="Close", command=quit)
        self.close_button.place(relx=0.78, rely=0.92, height=25)

        self.results_button = Button(master, text="Recover", command=self.old_job_check)
        self.results_button.place(relx=0.45, rely=0.92, height=25)

        self.text_box.tag_add("cool", '0.0', '1.0')
        self.text_box.tag_config("cool", foreground="black")
        self.text_box.tag_add("error", '0.0', '1.0')
        self.text_box.tag_config("error", foreground="red")

        self.recover()

    def getfile(self):
        self.file_path.set(askopenfilename(initialdir=self.home_dir,
                                           filetypes=[('Nexus files', '*.bay *.nex *.nexus'),
                                                      ('Text files', '*.txt'), ('All files', '*.*')],
                                           title="Select a file to submit to CIPRES server"))
        try:
            self.choose_file.config(textvariable=self.file_path)
            align = AlignIO.read(self.file_path.get(), format="nexus")
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "Alignment of " + str(len(align)) + " sequences of length " +
                                 str(align.get_alignment_length()) + ".\n", "cool")
            self.text_box.config(state=DISABLED)
            del align

            mb_block = []
            found = False
            with open(self.file_path.get(), 'r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    line = line.strip(' ')
                    line = line.rstrip(';')
                    if line.lower() == 'begin mrbayes':
                        found = True
                    if found:
                        mb_block.append(line)
            try:
                outgroup = False
                for item in mb_block:
                    if 'outgroup' in item.lower():
                        self.text_box.config(state=NORMAL)
                        self.text_box.insert(END, item + "\n\n", "cool")
                        self.text_box.config(state=DISABLED)
                        outgroup = True
                if not outgroup:
                    self.text_box.config(state=NORMAL)
                    self.text_box.insert(END, "You file has no outgroup defined!\n\n", "cool")
                    self.text_box.config(state=DISABLED)
                del outgroup
            except ValueError:
                pass
            del mb_block
            del found
        except FileNotFoundError:
            pass
        except NexusError:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "Nexus file is corrupted!\n", "error")
            self.text_box.insert(END, "Please, fix the file and try again!\n\n", "error")
            self.text_box.config(state=DISABLED)
        except ValueError:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "Wrong file type!\n\n", "error")
            self.text_box.config(state=DISABLED)

    def getconfig(self):
        conf = {'URL': 'https://cipresrest.sdsc.edu/cipresrest/v1', 'APPNAME': '', 'APPID': '', 'USERNAME': '',
                'PASSWORD': '', 'VERBOSE': ''}
        try:
            with open(join(self.home_dir, 'pycipres.conf'), 'r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    line = line.strip(' ')
                    (key, val) = line.split('=')
                    conf[key] = val
        except FileNotFoundError:
            pass
        return conf

    def recover(self):
        files = []
        for file in glob(join(dl_dir(), '*.pkl')):
            files.append(file)
        if files:
            self.results_button.configure(state=NORMAL)
        else:
            self.results_button.configure(state=DISABLED)

    def url_radio(self):
        """
        Verify the Checkbutton variable values and handles server_url entry state accordingly.
        """
        if self.url_val.get() == 0:
            self.server_url.configure(state=DISABLED)
        else:
            self.server_url.configure(state=NORMAL)

    def valid_radio(self):
        """
        Verify the Checkbutton variable values and handles validation status accordingly.
        """
        if self.valid_val.get() == 0:
            self.validate = False
        else:
            self.validate = True

    def mb_submit(self):
        login = cra.Client(appname=self.appname.get(), appID=self.appid.get(),
                           username=self.user.get(), password=self.passwd.get(),
                           baseUrl=self.server_url.get())
        vpar = {"toolId": "MRBAYES_XSEDE", "runtime_": 168, "mrbayesblockquery_": 1}
        file_name = self.choose_file.get()
        ipar = {"infile_": file_name}
        try:
            meta = {"statusEmail": "true", "clientJobName": splitext(basename(file_name))[0]}
            if self.validate:
                try:
                    job = login.submitJob(vParams=vpar, inputParams=ipar, metadata=meta,
                                          validateOnly=self.validate)
                    job_show(self, job, messages=True)
                except cra.ValidationError:
                    self.text_box.config(state=NORMAL)
                    self.text_box.insert(END, "Submission failed! Check you file and login information!\n\n", "error")
                    self.text_box.config(state=DISABLED)
            else:
                job = login.submitJob(vParams=vpar, inputParams=ipar, metadata=meta, validateOnly=self.validate)
                with open(join(dl_dir(), str(job.metadata['clientJobName'] + '.pkl')),
                          'wb') as f:
                    dump(job, f)
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, job_show(self, job) + "\n\n", "cool")
                self.text_box.config(state=DISABLED)
                get_results(self, job)
        except ConnectionError:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "No Internet connection!\nVerify your connection and try again!\n\n", "error")
            self.text_box.config(state=DISABLED)
        except cra.CipresError:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "CIPRES services are currently unavailable or you login information"
                                      " is incorrect!\n\n", "error")
            self.text_box.config(state=DISABLED)
        except FileNotFoundError:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "File not found!\n\n", "error")
            self.text_box.config(state=DISABLED)

    def old_job_check(self):
        try:
            files = []
            for file in glob(join(dl_dir(), '*.pkl')):
                files.append(file)
            if not files:
                pass
            else:
                for file in files:
                    with open(join(dl_dir(), file), 'rb') as f:
                        job = load(f)
                    job.update()
                    if not job.isDone():
                        self.text_box.config(state=NORMAL)
                        self.text_box.insert(END, job.messages[-1] + "\n", "cool")
                        self.text_box.insert(END, "Job " + job.metadata['clientJobName'] +
                                             " not finished yet!\nTry again later!\n", "cool")
                        self.text_box.config(state=DISABLED)
                    else:
                        get_results(self, job)
        except IndexError:
            pass
        except ConnectionError:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "No Internet connection. Try again later!\n", "error")
            self.text_box.config(state=DISABLED)
