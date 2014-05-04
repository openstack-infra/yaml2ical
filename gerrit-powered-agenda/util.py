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
import subprocess

import yaml

import const
from meeting import Meeting


"""Utility functions for check and gate jobs."""


def publish(meeting, ical):
    """Publish meeting information and ical file to wiki."""

    pass


def check_uniqueness():
    """Check for uniqueness in meeting room and time combination.  During gate
    job, we do not care about the meeting name.

    """

    # reads the current changes and verifies
    change_list = _read_yaml_files(const.DEFAULT_YAML_DIR)
    change_dict = _counting_dict_with(_make_schedule_key, change_list)

    # fails if duplicates exist
    if len(change_dict) == sum(change_dict.values()):
        return 0
    else:
        change_dict = _make_schedule_dict(_make_schedule_key,
                                          change_list,
                                          False)
        for key in change_dict:
            if len(change_dict[key]) > 1:
                meeting_quote = ['\'' + m + '\'' for m in change_dict[key]]
                meeting_str = ', '.join(meeting_quote)
                logging.info('Meetings %s are in conflict.' % (meeting_str))
        return 1


def check_conflicts():
    """Return whether the meeting would create scheduling conflicts. At this
    point, we are comparing the changes against the origin, while the meeting
    do matter.  If a meeting from the changes and a different meeting from the
    origin shares the same time, then we have a conflict.

    """

    # reads the current changes and verifies
    change_list = _read_yaml_files(const.DEFAULT_YAML_DIR)
    change_dict = _make_schedule_dict(_make_schedule_key, change_list, True)

    # runs the bash script to clone origin yaml files to .cache folder
    # then reads from the yaml files in the .cache folder
    subprocess.call(const.BASH_SCRIPT)
    origin_dict = _make_schedule_dict(_make_schedule_key,
                                      _read_yaml_files(const.CACHE_YAML_DIR),
                                      True)

    # make a set with all the meeting time
    meeting_time_set = set(list(change_dict.keys()) +
                           list(origin_dict.keys()))

    # compares the two, keep track of a conflict flag
    conflict = False  # doing this way so we can log all the conflicts
    for key in meeting_time_set:
        # both the changes and the original have this meeting time
        if key in change_dict and key in origin_dict:
            # and they are actually different meetings
            if change_dict[key] != origin_dict[key]:
                logging.info('Meetings \'%s\' and \'%s\' are in conflict.'
                             % (change_dict[key], origin_dict[key]))
                conflict = True

    if conflict:
        return 1
    return 0


def _read_yaml_files(directory):
    """Reads all the yaml in the given directory and returns a list of
    schedules times.

    :param directory: location of the yaml files
    :returns: list of schedules

    """

    os.chdir(directory)
    yaml_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and file.endswith(const.YAML_FILE_EXT):
            yaml_files.append(file)

    meetings = []
    for file in yaml_files:
        meetings.append(Meeting(yaml.load(open(file, 'r')), file))
    logging.info('Loaded %d meetings form YAML' % len(meetings))

    schedules = []
    for meeting in meetings:
        for schedule in meeting.get_schedule_tuple():
            schedules.append(schedule)

    os.chdir(const.SRC_DIR)
    return schedules


def _counting_dict_with(key_maker, list):
    """Make a counting dictionary. The key is obtained by a function applied to
    the element; the value counts the occurrence of the item in the list.

    :param key_maker: converts list items to strings
    :returns: counting dictionary

    """

    item_dict = {}
    for item in list:
        # just join the elements in the tuple together as key
        key = key_maker(item)
        if key in item_dict:
            item_dict[key] += 1
        else:
            item_dict[key] = 1
    return item_dict


def _make_schedule_dict(key_maker, list, replace_flag):
    """Make a schedule dictionary. The key is the time of the meeting. If
    replace_flag is true, then the value is the meeting name; otherwise, if
    replace_flag is false, the value is a list of meeting names.

    :param key_maker: converts list items to strings
    :param list: the list of schedules
    :param replace_flag: determines the value of the dictionary
    :returns: schedule dictionary

    """

    item_dict = {}
    for item in list:
        key = key_maker(item)
        if replace_flag:
            item_dict[key] = item[0]
        else:
            if key in item_dict:
                item_dict[key] += [item[0]]
            else:
                item_dict[key] = [item[0]]
    return item_dict


def _make_schedule_key(schedule):
    """A key making function for a schedule item.  The first item in the
    schedule is meeting name, followed by a tuple of time, day, and room.

    :param schedule: a schedule tuple
    :returns: string representation of the schedule tuple

    """

    schedule_time = schedule[1]
    schedules_str = [str(schedule_time[0]), schedule_time[1], schedule_time[2]]
    key = ''.join(schedules_str)
    return key
