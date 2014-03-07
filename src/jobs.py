import yaml
import icalendar
import pprint
import sys
import os
from meeting import Meeting

class MeetingJobs:
    """Executes post, gate, and check jobs."""

    yaml_dir = '../meetings'
    publish_url = '127.0.0.1'

    def execute_check(self):
        meetings = self.create_meetings(self.yaml_dir)
        meetings_display = "\n".join([m.display() for m in meetings])
        print(meetings_display) # testing purpose
        # now convert meetings to a list of ical

    def execute_gate(self):
        pass

    def execute_post(self):
        pass

    def create_meetings(self, yaml_dir):
        os.chdir(yaml_dir)
        meetings_yaml = [yaml.load(open(f, 'r')) for f in os.listdir() if os.path.isfile(f) and ".yaml" in f]
        meetings = [Meeting(y) for y in meetings_yaml]
        return meetings

def pprint_yaml():
    """For now, this is a simple script to import all the yaml files and pretty print it."""

    # change the current directory to the meetings directory where all the yaml files are located
    os.chdir('../meetings/')

    # get a list of all the yaml files
    meetings = [yaml.load(open(f, 'r')) for f in os.listdir() if os.path.isfile(f) and ".yaml" in f]

    for m in meetings:
        print(yaml.dump(m))

# entry point
#pprint_yaml()
jobs = MeetingJobs()
jobs.execute_check()
