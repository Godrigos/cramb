#!/usr/bin/env python

from tkinter import *


def job_show(self, job, messages=True):
    """ A debugging method to dump some of the content of this object to text_box entry """

    if not job.jobHandle and job.commandline:
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "Submission validated.  Commandline is: '%s'" % job.commandline + '\n', "cool")
        self.text_box.config(state=DISABLED)

    string = str("Job=" + job.jobHandle)
    if job.terminalStage:
        if job.failed:
            string += str(", failed at stage " + job.jobStage + '\n')
        else:
            string += str(", finished, results are at " + job.resultsUrl + '\n')
    else:
        string += str(", not finished, stage=" + job.jobStage + '\n')
    self.text_box.config(state=NORMAL)
    self.text_box.insert(END, string, "cool")
    self.text_box.config(state=DISABLED)
    if messages:
        for m in job.messages:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "\t" + m + "\n", "cool")
            self.text_box.config(state=DISABLED)
        if job.metadata:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "Metadata:\n", "cool")
            for key, value in job.metadata.items():
                self.text_box.insert(END, "\t" + key + ': ' + value + '\n', "cool")
            self.text_box.config(state=DISABLED)
        else:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "There is no metadata.\n", "cool")
            self.text_box.config(state=DISABLED)
