#!/usr/bin/env python

### for now, this is a simple script to import all the yaml files and pretty print it

import yaml
import pprint
import sys
from os import listdir, chdir
from os.path import isfile, dirname, join

# change the current directory to the meetings directory where all the yaml files are located
os.chdir('../meetings/')

# get a list of all the yaml files
yamlfiles = [f for f in os.listdir() if os.path.isfile(f) and ".yaml" in f]

meeting = []
for f in yaml:
    m = open(f, 'r')

    meeting.append(yaml.load(m))

    # print yaml.load(meeting), used to have sys.out as second before to print to terminal
    print yaml.dump(yaml.load(m))
