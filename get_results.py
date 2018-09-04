#!/usr/bin/env python

"""
This file is part of CRAMrBayesT.

CRAMrBayesT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CRAMrBayesT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CRAMrBayesT.  If not, see <https://www.gnu.org/licenses/>.

Copyright 2018 Rodrigo Aluizio    
"""

import sys
from time import sleep
from os import makedirs, remove
from os.path import exists, join
from requests.exceptions import ConnectionError
# from print_progress import print_progress
from download_folder_path import get_download_path as dl_dir


def get_results(job):
    """
    While loop that evaluates Job status and download the result
    when the job is complete.
    """
    try:
        job.update()
        while not job.isDone():
            sleep(600)
            try:
                job.update()
                print(job.messages[-1])
            except ConnectionError:
                print("Connection lost! Will keep trying!")
                pass
        else:
            # Create a directory to store the results
            dld = join(dl_dir(), str(job.metadata['clientJobName']))
        
            if not exists(dld):
                makedirs(dld)
            print("\nDownloading results of", str(job.metadata['clientJobName']))
        
            resultFiles = job.listResults(final=True)
            i = 0
        
            try:
                for filename in resultFiles:
                    resultFiles[filename].download(directory=dld)
                    # print_progress(i, len(resultFiles)-1, bar_length=60)
                    i += 1
            except ConnectionError:
                print("Connection lost!")
                print("Press Enter to exit ...")
                input()
                sys.exit(1)
        
            job.delete()
            print("\nJob completed and files downloaded!")
            print("Press Enter to exit ...")
            remove(join(dl_dir(), str(job.metadata['clientJobName'] + '.pkl')))
            input()
    except KeyboardInterrupt:
        print("\nYou have canceled the result watching. You will have to " +
              "retrieve the results manually.\nUse your '.pkl' file.")
        print("Press Enter to exit ...")
        input()
        sys.exit(1)
