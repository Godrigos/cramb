#!/usr/bin/env python

from tkinter import *


def job_show(self, job, messages=True):
    """ A debugging method to dump some of the content of this object to text_box entry """

    if not job.jobHandle and job.commandline:
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "Submission validated.  Commandline is: '%s'" % job.commandline + '\n', "cool")
        self.text_box.config(state=DISABLED)

    string = "Job=%s" % job.jobHandle
    if job.terminalStage:
        if job.failed:
            string += ", failed at stage %s" % job.jobStage + '\n'
        else:
            string += ", finished, results are at %s" % job.resultsUrl + '\n'
    else:
        string += ", not finished, stage=%s" % job.jobStage + '\n'
    self.text_box.config(state=NORMAL)
    self.text_box.insert(END, string, "cool")
    self.text_box.config(state=DISABLED)
    if messages:
        for m in job.messages:
            self.text_box.config(state=NORMAL)
            self.text_box.insert("\t" + m, "cool")
            self.text_box.config(state=DISABLED)
        if job.metadata:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "Metadata:", "cool")
            for key in job.metadata:
                self.text_box.insert(END, "\t" + job.metadata, "cool")
            self.text_box.config(state=DISABLED)
        else:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "There is no metadata.\n", "cool")
            self.text_box.config(state=DISABLED)