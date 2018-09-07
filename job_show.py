#!/usr/bin/env python


def job_show(job, messages=True):
    msg = ""
    string = ""
    """ A debugging method to dump some of the content of this object to text_box entry """
    if not job.jobHandle and job.commandline:
        string = str("Submission validated.  Commandline is: " + job.commandline + '\n')
    elif job.jobHandle and job.commandline:
        string = str("Job=" + job.jobHandle)
    elif job.terminalStage:
        if job.failed:
            string += str(", failed at stage " + job.jobStage + '\n')
        else:
            string += str(", finished, results are at " + job.resultsUrl + '\n')
    else:
        string += str(", not finished, stage=" + job.jobStage + '\n')

    if messages:
        for m in job.messages:
            msg += "\t" + m + "\n"
        if job.metadata:
            msg += "Metadata:\n"
            for key, value in job.metadata.items():
                msg += "\t" + key + ': ' + value + '\n'
        else:
            msg = "There is no metadata.\n"

    return string + msg
