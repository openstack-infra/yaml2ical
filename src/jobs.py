import yaml
import icalendar
import pprint
import sys
import os

class MeetingJobs:
    """Executes post, gate, and check jobs."""

    # make this a singleton?
    
    def __init__(self, publish_url):
        self.publish_url = publish_url

    def execute_check():
        pass

    def execute_gate():
        pass

    def execute_post():
        pass

def pprint_yaml():
    """For now, this is a simple script to import all the yaml files and pretty print it."""

    # change the current directory to the meetings directory where all the yaml files are located
    os.chdir('../meetings/')

    # get a list of all the yaml files
    meetings = [yaml.load(open(f, 'r')) for f in os.listdir() if os.path.isfile(f) and ".yaml" in f]

    for m in meetings:
        print(yaml.dump(m))

# main
pprint_yaml()

