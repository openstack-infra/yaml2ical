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

import datetime
import hashlib
import os
import yaml


class Schedule:
    """A meeting schedule."""

    def __init__(self, sched_yaml):
        """Initialize schedule from yaml."""

        self.time = datetime.datetime.strptime(sched_yaml['time'], '%H%M')
        self.day = sched_yaml['day']
        self.irc = sched_yaml['irc']
        self.freq = sched_yaml['frequency']


class Meeting:
    """An OpenStack meeting."""

    def __init__(self):
        """Initialize meeting from yaml file name 'filename'."""
        pass


def load_meetings(yaml_source):
    """Build YAML object and load meeting data

    :param yaml_source: source data to load, which can be a directory or
                        stream.
    :returns: list of meeting objects
    """
    meetings_yaml = []
    # Determine what the yaml_source is
    if os.path.isdir(yaml_source):
        # TODO(lbragstad): use os.path.walk?
        for f in os.listdir(yaml_source):
            # Build the entire file path and append to the list of yaml
            # meetings
            yaml_file = os.path.join(yaml_source, f)
            meetings_yaml.append(yaml_file)
    elif isinstance(yaml_source, str):
        return [_load_meeting(yaml_source)]
    else:
        # If we don't have a .yaml file, a directory of .yaml files, or any
        # YAML data fail out here.
        raise ValueError("YAML source isn't a .yaml file, directory "
                         "containing .yaml files, or YAML data.")

    meetings = []
    for yaml_file in meetings_yaml:
        with open(yaml_file, 'r') as f:
            meetings.append(_load_meeting(f))

    return meetings


def _load_meeting(meeting_yaml):
    yaml_obj = yaml.safe_load(meeting_yaml)
    m = Meeting()

    # Build meeting attributes from yaml
    m.chair = yaml_obj['chair']
    m.description = yaml_obj['description']
    m.project = yaml_obj['project']
    m._filename = (yaml_obj['project'] + '-' +
                   hashlib.md5(str(yaml_obj).encode('utf-8')).hexdigest()[:8])

    # TODO(lbragstad): See if there is another way we can do this instead
    # of having every Meeting object build a list of Schedule objects.
    m.schedules = []
    for sch in yaml_obj['schedule']:
        s = Schedule(sch)
        m.schedules.append(s)

    return m


class MeetingConflictError(Exception):
    pass


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


def check_for_meeting_conflicts(meetings):
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
                    msg_dict = {'first': current_meeting['filename'],
                                'second': next_meeting['filename']}
                    raise MeetingConflictError("Conflict between %(first)s "
                                               "and %(second)s." % msg_dict)
