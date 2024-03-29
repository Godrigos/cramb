# cramb

CIPRES API - MrBayes Submission Client

[![Github Releases](https://img.shields.io/github/downloads/Godrigos/cramb/total.svg?style=flat-square)](https://github.com/Godrigos/cramb/releases)
[![GitHub release](https://img.shields.io/github/release/Godrigos/cramb.svg?style=flat-square)](https://github.com/Godrigos/cramb/releases/latest)

cramb is a [Python 3](https://www.python.org)
application with a GUI built using Tkinter.
It is intended to ease the process of sending a Nexus
file to [CIPRES](https://www.phylo.org/restusers)
servers for a bayesian phylogenetic
inference (using MrBayes) and then retrieve the results.
It assumes your Nexus file has a MrBayes
[Block](https://en.wikipedia.org/wiki/Nexus_file)
correctly configured along with the data to be analysed.

Here is an example of a MrBayes Block inside a Nexus
File:
```nexus
begin mrbayes;
    set autoclose=yes nowarn=yes;
    charset Locus1 = 1-100;
    charset Locus2 = 101-200;
    partition Multi = 2: Locus1, Locus2;
    set partition = Multi;
    lset applyto=(1) nst=6 rates=invgamma;
    lset applyto=(2) nst=6 rates=gamma;
    prset applyto=(2) statefreqpr=fixed(equal);
    outgroup 1;
    mcmc ngen=500000 printfreq=1000 samplefreq=100 nchains=4 temp=0.5 savebrlens=yes;
    sumt relburnin=yes burninfrac=0.25 contype=halfcompat conformat=simple;
END;
 ```

More information on the application usage, can be found
[here](https://github.com/Godrigos/cramb/wiki). 
