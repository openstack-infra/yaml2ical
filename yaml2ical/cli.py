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
from yaml2ical import index
from yaml2ical import meeting


# logging settings
logging.basicConfig(format='%(asctime)s  - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def parse_args():
    # build option parser:
    description = """
A tool that automates the process for testing, integrating, and
publishing changes to online meeting schedules.
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
    parser.add_argument("-t", "--indextemplate",
                        dest="index_template",
                        help="generate an index from selected meetings")
    parser.add_argument("-w", "--indexoutput",
                        dest="index_output",
                        help="output index file")
    parser.add_argument("-n", "--name",
                        dest="calname",
                        help="name of calendar to set within the ical")
    parser.add_argument("-d", "--description",
                        dest="caldescription",
                        help="description of calendar to set within the ical")
    parser.add_argument("-f", "--force",
                        dest="force",
                        action='store_true',
                        help="remove/overwrite previous output files")

    # parse arguments:
    args = parser.parse_args()

    if ((args.index_template and not args.index_output) or
       (args.index_output and not args.index_template)):
        parser.error("You need to provide both -t and "
                     "-w if you want to output an index.")
    if args.ical_dir and (args.calname or args.caldescription):
        parser.error("Name/Description and single ical per meeting "
                     "(-i) is incompatiable due to spec.")

    return args


def _check_if_location_exists(location, style='f'):
    if style == 'd' and not os.path.isdir(location):
        raise ValueError("Directory %s does not exist" % location)
    if style == 'f' and not os.path.isfile(location):
        raise ValueError("File %s does not exist" % location)


def _prepare_output(output, style='f', force=False):
    location = os.path.abspath(output)
    if style == 'd':
        _check_if_location_exists(location, style=style)
        if os.listdir(location) != []:
            if force:
                for f in os.listdir(location):
                    file_path = os.path.join(location, f)
                    os.remove(file_path)
            else:
                raise Exception("Directory for storing iCals is not empty, "
                                "suggest running with -f to remove old files.")
    else:
        if os.path.exists(location):
            if force:
                os.remove(location)
            else:
                raise Exception("Output file already exists, suggest running "
                                "with -f to overwrite previous file.")
    return location


def main():
    args = parse_args()

    yaml_dir = os.path.abspath(args.yaml_dir)
    _check_if_location_exists(yaml_dir, style='d')

    meetings = meeting.load_meetings(yaml_dir)
    # Check uniqueness and conflicts here before writing out to .ics
    meeting.check_for_meeting_conflicts(meetings)

    if args.ical_dir:
        ical_dir = _prepare_output(args.ical_dir, style='d', force=args.force)
        ical.convert_meetings_to_ical(meetings, outputdir=ical_dir)
    else:
        icalfile = _prepare_output(args.icalfile, force=args.force)
        ical.convert_meetings_to_ical(meetings, outputfile=icalfile,
                                      caldescription=args.caldescription,
                                      calname=args.calname)

    if args.index_template and args.index_output:
        index_template = os.path.abspath(args.index_template)
        _check_if_location_exists(index_template)
        index_output = _prepare_output(args.index_output, force=args.force)
        index.convert_meetings_to_index(
            meetings, index_template, index_output)


if __name__ == '__main__':
    main()
