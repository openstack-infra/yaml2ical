#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
import util


# logging settings
logging.basicConfig(format='%(asctime)s  - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class MeetingJobs:
    """Executes post, gate, and check jobs."""

    def execute_check(self):
        """Execute check job."""

        logging.info('Check job initiated.')
        meetings = self.retrieve_meetings(const.YAML_DIR)

        # convert meetings to a list of ical
        for m in meetings:
            m.write_ical()
            logging.info('Wrote %d meetings to iCal' % (len(meetings)))

        os.chdir(const.SRC_DIR)
        if util.check_uniqueness() == 0:
            if util.check_conflicts() == 0:
                logging.info('Check job finished.')
                return 0
        logging.info('Check job finished.')
        return 1

    def execute_gate(self):
        """Execute gate job."""

        logging.info('Gate job initiated.')
        os.chdir(const.SRC_DIR)
        result = util.check_conflicts()
        logging.info('Gate job finished.')
        return result

    def execute_post(self):
        """Execute post job."""

        logging.info('Post job initiated.')
        meetings = self.retrieve_meetings(const.YAML_DIR)

        # convert meetings to a list of ical
        for m in meetings:
            m.write_ical()
        logging.info('Wrote %d meetings to iCal' % (len(meetings)))
        logging.info('Post job finished.')


def retrieve_meetings(self, yaml_dir):
    """Return a list of Meetings initialized from files in yaml_dir."""

    os.chdir(yaml_dir)
    meetings_yaml = [f for f in os.listdir()
                     if os.path.isfile(f) and
                     f.endswith(const.YAML_FILE_EXT)]
    meetings = [Meeting(yaml.load(open(f, 'r')), f)
                for f in meetings_yaml]
    logging.info('Loaded %d meetings from YAML' % (len(meetings)))
    os.chdir(const.SRC_DIR)
    return meetings

# entry point
jobs = MeetingJobs()
jobs.execute_check()
