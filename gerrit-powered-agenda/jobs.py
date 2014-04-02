#! /usr/bin/env python
#
#    Copyright 2014 North Dakota State University
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import os
import yaml

import const
from meeting import Meeting

# logging settings
logging.basicConfig(format='%(asctime)s  - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

yaml_dir = '../meetings'
ical_dir = '../icals'
# NOTE(jotan): publish_url should be changed to the wiki URL eventually
publish_url = '127.0.0.1'


class MeetingJobs:
    """Executes post, gate, and check jobs."""

    def execute_check(self):
        """Execute check job."""

        logging.info('Check job initiated.')
        meetings = self.retrieve_meetings(yaml_dir)

        # convert meetings to a list of ical
        for m in meetings:
            m.write_ical()
        logging.info('Wrote %d meetings to iCal' % (len(meetings)))
        logging.info('Check job finished.')

    def execute_gate(self):
        """Execute gate job."""

        pass

    def execute_post(self):
        """Execute post job."""

        pass

    def retrieve_meetings(self, yaml_dir):
        """Return a list of Meetings initialized from files in yaml_dir."""

        os.chdir(yaml_dir)
        meetings_yaml = [f for f in os.listdir()
                         if os.path.isfile(f) and
                         f.endswith(const.YAML_FILE_EXT)]
        meetings = [Meeting(yaml.load(open(f, 'r')), f)
                    for f in meetings_yaml]
        logging.info('Loaded %d meetings from YAML' % (len(meetings)))
        return meetings

# entry point
jobs = MeetingJobs()
jobs.execute_check()
