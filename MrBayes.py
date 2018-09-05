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
    
# Import the needed modules.
import sys
from glob import glob
import python_cipres.client as CRA
from dill import dump, load
from time import sleep
from os.path import isfile, splitext, basename, join
from requests.exceptions import ConnectionError
from download_folder_path import get_download_path as dl_dir
from get_results import get_results

# CIPRES API credentials needed to connect and submit jobs.
try:
    App = CRA.Application().getProperties()
except Exception:
    print("Could not find pycipres.conf, make sure it exists and is in\n" +
	      "right directory with the right content!")
    print("Press Enter to exit ...")
    input()
    sys.exit(1)

Login = CRA.Client(App.APPNAME, App.APPID, App.USERNAME, App.PASSWORD, App.URL)

# Verify if there is a job which results were not yet downloaded
try:
    files = []
    for file in glob(join(dl_dir(), '*.pkl')):
        files.append(file)
    if not files:
        pass
    else:
        print("You have results from previous analysis to download!")
        for file in files:
            with open(join(dl_dir(), file), 'rb') as f:
                job = load(f)
            get_results(job)
        exit(0)
except IndexError:
    pass
    

# Analysis run parameters. The 'toolId' entry refers to the tool being used.
vPar = {"toolId": "MRBAYES_XSEDE", "runtime_": 168, "mrbayesblockquery_": 1}

# Define the name of the file that stores the data and parameters
# of the analysis.
try:
    file_name = input("Enter the name of the file to analyze: ")
    while not isfile(file_name):
        print("Error accessing file. Check file name and path and try again.")
        file_name = input("Enter the name of the file to analyze: ")
    iPar = {"infile_": file_name}
    # Define a name for the analysis in the server.
    meta = {"statusEmail": "true",
            "clientJobName": splitext(basename(file_name))[0]}
except KeyboardInterrupt:
    print("\nYou have canceled CRAMrBayesT!")
    print("Closing now!")
    sleep(3)
    exit(0)

# Job submission. If you want to validate the job before submitting
# chance 'validateOnly' to True.
try:
    job = Login.submitJob(vParams=vPar, inputParams=iPar, metadata=meta,
                          validateOnly=True)
    job.show(messages=True)
except ConnectionError:
    print("\nNo working internet connection to submit the analysis!\n" +
          "Please connect to the internet and try again!")
    print("Press Enter to exit ...")
    input()
    sys.exit(1)
except CRA.CipresError:
    print("CIPRES services are unavailable, try again later!")
    print("Press Enter to exit ...")
    input()
    sys.exit(1)

# Job backup file, useful if the terminal is closed before job
# completion. It can be used to manually retrieve results in
# a later moment.
with open(join(dl_dir() , str(job.metadata['clientJobName'] + '.pkl')),
                              'wb') as f:
    dump(job, f)

# Get results
get_results(job)

