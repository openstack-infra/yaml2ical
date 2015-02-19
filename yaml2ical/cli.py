# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import logging
import os

from yaml2ical import ical


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
    outputtype = parser.add_mutually_exclusive_group(required=True)
    outputtype.add_argument("-i", "--icaldir",
                            dest="ical_dir",
                            help="output directory (one file per meeting)")
    outputtype.add_argument("-o", "--output",
                            dest="icalfile",
                            help="output file (one file for all meetings)")
    parser.add_argument("-f", "--force",
                        dest="force",
                        action='store_true',
                        help="forcefully remove/overwrite previous .ics "
                             "output files")

    # parse arguments:
    return parser.parse_args()


def _check_if_location_exists(location):
    if not os.path.isdir(location):
        raise ValueError("Invalid location %s" % location)


def main():
    args = parse_args()

    yaml_dir = os.path.abspath(args.yaml_dir)
    _check_if_location_exists(yaml_dir)
    if args.ical_dir:
        ical_dir = os.path.abspath(args.ical_dir)
        _check_if_location_exists(ical_dir)

        if os.listdir(ical_dir) != []:
            if args.force:
                for f in os.listdir(ical_dir):
                    file_path = os.path.join(ical_dir, f)
                    os.remove(file_path)
            else:
                raise Exception("Directory for storing iCals is not empty, "
                                "suggest running with -f to remove old files.")
        ical.convert_yaml_to_ical(yaml_dir, outputdir=ical_dir)
    else:
        icalfile = os.path.abspath(args.icalfile)
        if os.path.exists(icalfile):
            if args.force:
                os.remove(icalfile)
            else:
                raise Exception("Output file already exists, suggest running "
                                "with -f to overwrite previous file.")
        ical.convert_yaml_to_ical(yaml_dir, outputfile=icalfile)


if __name__ == '__main__':
    main()
