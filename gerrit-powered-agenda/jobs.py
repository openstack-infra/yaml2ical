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


def execute_check():
    """Execute check job."""

    logging.info('Check job initiated.')

    # NOTE(jotan): once a CLI parameter for YAML_DIR has been
    # implemented, only use DEFAULT_YAML_DIR if the parameter has
    # not been supplied
    yaml_dir = const.DEFAULT_YAML_DIR

    meetings = __load_meetings(yaml_dir)

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


def execute_gate():
    """Execute gate job."""

    logging.info('Gate job initiated.')
    os.chdir(const.SRC_DIR)
    result = util.check_conflicts()
    logging.info('Gate job finished.')
    return result


def execute_post():
    """Execute post job."""

    logging.info('Post job initiated.')
    yaml_dir = const.DEFAULT_YAML_DIR
    meetings = __load_meetings(yaml_dir)

    # convert meetings to a list of ical
    for m in meetings:
        m.write_ical()
    logging.info('Wrote %d meetings to iCal' % (len(meetings)))
    logging.info('Post job finished.')


def __load_meetings(yaml_dir):
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
execute_check()
