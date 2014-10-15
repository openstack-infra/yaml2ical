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

import logging
import os

from arbiter import meeting

"""Utility functions."""


def _extract_meeting_info(meeting_obj):
    """Pull out meeting info of Meeting object.

    :param meeting_obj: Meeting object
    :returns: a dictionary of meeting info

    """
    meeting_info = []
    for schedule in meeting_obj.schedules:
        info = {'name': meeting_obj.project,
                'filename': meeting_obj._filename,
                'day': schedule.day,
                'time': schedule.time,
                'irc_room': schedule.irc}
        meeting_info.append(info)

    return meeting_info


def _check_for_meeting_conflicts(meetings):
    """Check if a list of meetings have conflicts.

    :param meetings: list of Meeting objects

    """

    for i in range(len(meetings)):
        meeting_info = _extract_meeting_info(meetings[i])
        for j in range(i + 1, len(meetings)):
            next_meeting_info = _extract_meeting_info(meetings[j])
            for current_meeting in meeting_info:
                for next_meeting in next_meeting_info:
                    if current_meeting['day'] != next_meeting['day']:
                        continue
                    if current_meeting['time'] != next_meeting['time']:
                        continue
                    if current_meeting['irc_room'] != next_meeting['irc_room']:
                        continue
                    logging.error("Conflict between %s and %s" % (
                        current_meeting['filename'], next_meeting['filename']))


def convert_yaml_to_ical(yaml_dir, outputdir=None, outputfile=None):
    """Convert meeting YAML files to iCal.

    If meeting_list is specified, only those meetings in yaml_dir with
    filenames contained in meeting_list are converted; otherwise,
    all meeting in yaml_dir are converted.

    :param yaml_dir: directory where meeting.yaml files are stored
    :param outputdir: location to store iCal files (one file per meeting)
    :param outputfile: output iCal file (one single file for all meetings)

    """
    meetings = meeting.load_meetings(yaml_dir)

    # Check uniqueness and conflicts here before writing out to .ics
    _check_for_meeting_conflicts(meetings)

    # convert meetings to a list of ical
    if outputdir:
        for m in meetings:
            cal = meeting.GerritPoweredCalendar()
            m.add_to_calendar(cal)
            filename = os.path.basename(m._filename).split('.')[0] + '.ics'
            cal.write_to_disk(os.path.join(outputdir, filename))

    # convert meetings into a single ical
    if outputfile:
        cal = meeting.GerritPoweredCalendar()
        for m in meetings:
            m.add_to_calendar(cal)
        cal.write_to_disk(outputfile)

    # TODO(jotan): verify converted ical is valid
    logging.info('Wrote %d meetings to iCal' % (len(meetings)))
