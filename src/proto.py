#!/usr/bin/env python

import yaml
import pprint
import sys

meeting = open("meeting.yaml", 'r')
# print yaml.load(meeting)
yaml.dump(yaml.load(meeting), sys.out)