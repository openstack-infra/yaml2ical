#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright 2014 OpenStack Foundation
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

import argparse
import logging
import os

from arbiter import util


# logging settings
logging.basicConfig(format='%(asctime)s  - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def parse_args():
    # build option parser:
    description = """
A tool that automates the process for testing, integrating, and
publishing changes to OpenStack meetings using the existing OpenStack
project infrastructure.
"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description)

    parser.add_argument("-y", "--yamldir",
                        dest="yaml_dir",
                        required=True,
                        help="directory containing YAML to process")
    parser.add_argument("-i", "--icaldir",
                        dest="ical_dir",
                        required=True,
                        help="directory to store converted iCal")
    parser.add_argument("-f", "--force",
                        dest="force",
                        action='store_true',
                        help="forcefully remove old .ics files from iCal "
                             "directory")

    # parse arguments:
    return parser.parse_args()


def _check_if_location_exists(location):
    if not os.path.isdir(location):
        raise ValueError("Invalid location %s" % location)


def main():
    args = parse_args()

    force = args.force
    yaml_dir = os.path.abspath(args.yaml_dir)
    _check_if_location_exists(yaml_dir)
    ical_dir = os.path.abspath(args.ical_dir)
    _check_if_location_exists(ical_dir)

    if os.listdir(ical_dir) != []:
        if force:
            for f in os.listdir(ical_dir):
                file_path = os.path.join(ical_dir, f)
                os.remove(file_path)
        else:
            raise Exception("Directory for storing iCals is not empty, suggest"
                            " running with -f to remove old iCal files.")

    # Convert yaml to iCal
    util.convert_yaml_to_ical(yaml_dir, ical_dir)


if __name__ == '__main__':
    main()
