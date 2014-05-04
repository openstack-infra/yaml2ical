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
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os

import const
import util


# logging settings
logging.basicConfig(format='%(asctime)s  - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def execute_check(yaml_dir, ical_dir):
    """Execute check job."""

    logging.info('Check job initiated.')

    # convert meetings to a list of ical
    util.convert_yaml_to_ical(yaml_dir, ical_dir)

    os.chdir(const.SRC_DIR)
    if util.check_uniqueness() == 0:
        if util.check_conflicts() == 0:
            logging.info('Check job finished.')
            return 0
    logging.info('Check job finished.')
    return 1


def execute_gate(yaml_dir):
    """Execute gate job."""

    logging.info('Gate job initiated.')
    os.chdir(const.SRC_DIR)
    result = util.check_conflicts()
    logging.info('Gate job finished.')
    return result


def execute_post(yaml_dir, ical_dir, publish_url):
    """Execute post job."""

    logging.info('Post job initiated.')

    # convert meetings to a list of ical
    util.convert_yaml_to_ical(yaml_dir, ical_dir)

    logging.info('Post job finished.')

# entry point
if __name__ == '__main__':

    # build option parser:
    description = """
A tool that automates the process for testing, integrating, and
publishing changes to OpenStack meetings using the existing OpenStack
project infrastructure.
"""

    epilog = """
This program is meant to be invoked as a Jenkins job during check,
gate, and post tests. Depending on which test invokes the program,
it will perform different activites.

Check:
    - Verify correct YAML syntax for proposed meeting changes.
    - Verify YAML files can be converted to valid iCal files
    - Test that proposed changes would not result in scheduling
      conflicts

Gate:
    - Test that proposed changes would not result in scheduling
      conflicts (including conflicts with changes that have been
      made since the inital check test).

Post:
    - Convert YAML files to iCal files
    - Publish meeting changes and associated iCal files to a
      public wiki location
"""
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog)

    parser.add_argument("-t", "--test",
                        help="test to execute. valid values are check,\
                        gate, and post.")
    parser.add_argument("-c", "--convert",
                        action="store_true",
                        default=False,
                        help="convert meeting YAML to iCal format.")
    parser.add_argument("-y", "--yamldir",
                        dest="yaml_dir",
                        default=const.DEFAULT_YAML_DIR,
                        help="directory containing YAML to process")
    parser.add_argument("-m", "--meetings",
                        dest="meeting_list_file",
                        help="name of file containing meetings to \
                        process. meetings are specified by filename,\
                        which correspond to meeting filenames in\
                        yamldir. filenames should be separated by\
                        newlines.")
    parser.add_argument("-i", "--icaldir",
                        dest="ical_dir",
                        default=const.DEFAULT_ICAL_DIR,
                        help="directory to store converted iCal")

    # parse arguments:
    args = parser.parse_args()

    test = args.test
    convert = args.convert
    yaml_dir = args.yaml_dir
    meeting_list_file = args.meeting_list_file
    ical_dir = args.ical_dir

    if (yaml_dir and not os.path.isdir(yaml_dir)):
        parser.error("invalid YAML directory provided")
    if (ical_dir and not os.path.isdir(ical_dir)):
        parser.error("invalid iCal directory provided")

    if not test and not convert:
        parser.error(
            "invalid arguments. must specify test or convert")
    elif test:
        if test == "check":
            execute_check(yaml_dir, ical_dir)
        elif test == "gate":
            execute_gate(yaml_dir)
        elif test == "post":
            execute_post(yaml_dir, ical_dir, const.PUBLISH_URL)
        else:
            parser.error("invalid test provided")
    elif convert:
        # if file containing list of meetings provided
        if meeting_list_file:
            if not os.path.isfile(meeting_list_file):
                parser.error("meeting list file does not exist")
            util.convert_yaml_to_ical(yaml_dir,
                                      ical_dir,
                                      meeting_list_file)
        else:
            # convert all meetings in yaml_dir
            util.convert_yaml_to_ical(yaml_dir, ical_dir)
