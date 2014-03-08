import yaml
import icalendar
import pprint
import sys
import os
import uuid
from meeting import Meeting
import logging

# logging settings
logging.basicConfig(format='%(asctime)s  - %(levelname)s - %(message)s', level=logging.DEBUG)

yaml_dir = '../meetings'
ical_dir = '../icals'
publish_url = '127.0.0.1'

# should we make execute_gate(), etc. static methods instead?
class MeetingJobs:
    """Executes post, gate, and check jobs."""

    def execute_check(self):
        logging.info('Check job initiated.')
        meetings = self.load_meetings(yaml_dir)

        # now convert meetings to a list of ical
        for m in meetings:
            m.write_ical()
        logging.info('Wrote %d meetings to iCal' % (len(meetings)))
        logging.info('Check job finished.')

    def execute_gate(self):
        pass

    def execute_post(self):
        pass

    def load_meetings(self, yaml_dir):
        os.chdir(yaml_dir)
        meetings_yaml = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('yaml')]
        meetings = [Meeting(yaml.load(open(f, 'r')), f) for f in meetings_yaml]
        logging.info('Loaded %d meetings from YAML' % (len(meetings)))
        return meetings

def pprint_yaml():
    """For now, this is a simple script to import all the yaml files and pretty print it."""

    # change the current directory to the meetings directory where all the yaml files are located
    os.chdir(yaml_dir)

    # get a list of all the yaml files
    meetings = [yaml.load(open(f, 'r')) for f in os.listdir() if os.path.isfile(f) and ".yaml" in f]

    for m in meetings:
        print(yaml.dump(m))

# entry point
jobs = MeetingJobs()
jobs.execute_check()
