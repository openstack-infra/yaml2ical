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

import datetime
import hashlib
import os

import icalendar
import pytz
import yaml

from arbiter import const
from arbiter import schedule


class Meeting:
    """An OpenStack meeting."""

    def __init__(self):
        """Initialize meeting from yaml file name 'filename'."""
        pass

    def write_ical(self, ical_dir):
        """Write this meeting to disk using the iCal format."""

        cal = icalendar.Calendar()

        # add properties to ensure compliance
        cal.add('prodid', '-//OpenStack//Gerrit-Powered Meeting Agendas//EN')
        cal.add('version', '2.0')

        for sch in self.schedules:
            # one Event per iCal file
            event = icalendar.Event()

            # NOTE(jotan): I think the summary field needs to be unique per
            # event in an ical file (at least, for it to work with
            # Google Calendar)

            event.add('summary', self.project + ' (' + sch.irc + ')')

            # add ical description
            project_descript = "Project:  %s" % (self.project)
            chair_descript = "Chair:  %s" % (self.chair)
            irc_descript = "IRC:  %s" % (sch.irc)
            agenda_yaml = yaml.dump(self.agenda, default_flow_style=False)
            agenda_descript = "Agenda:\n%s\n" % (agenda_yaml)
            descript_descript = "Description:  %s" % (self.description)
            ical_descript = "\n".join((project_descript,
                                       chair_descript,
                                       irc_descript,
                                       agenda_descript,
                                       descript_descript))
            event.add('description', ical_descript)

            # get starting date
            d = datetime.datetime.utcnow()
            next_meeting = self._next_weekday(d, const.WEEKDAYS[sch.day])

            next_meeting_dt = datetime.datetime(next_meeting.year,
                                                next_meeting.month,
                                                next_meeting.day,
                                                sch.time.hour,
                                                sch.time.minute,
                                                tzinfo=pytz.utc)
            event.add('dtstart', next_meeting_dt)

            # add recurrence rule
            event.add('rrule', {'freq': sch.freq})

            # add meeting length
            # TODO(jotan): determine duration to use for OpenStack meetings
            event.add('duration', datetime.timedelta(hours=1))

            # add event to calendar
            cal.add_component(event)

        # determine file name from source file
        ical_filename = os.path.basename(self._filename).split('.')[0] + '.ics'
        ical_filename = os.path.join(ical_dir, ical_filename)

        # write ical files to disk
        with open(ical_filename, 'wb') as ics:
            ics.write(cal.to_ical())

    def _next_weekday(self, ref_date, weekday):
        """Return the date of the next meeting.

        :param ref_date: datetime object of meeting
        :param weekday: weekday the meeting is held on

        :returns: datetime object of the next meeting time
        """

        days_ahead = weekday - ref_date.weekday()
        if days_ahead <= 0:  # target day already happened this week
            days_ahead += 7
        return ref_date + datetime.timedelta(days_ahead)


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
    m.agenda = yaml_obj['agenda']
    m.chair = yaml_obj['chair']
    m.description = yaml_obj['description']
    m.project = yaml_obj['project']
    m._filename = (yaml_obj['project'] + '-' +
                   hashlib.md5(str(yaml_obj).encode('utf-8')).hexdigest()[:8])

    # TODO(lbragstad): See if there is another way we can do this instead
    # of having every Meeting object build a list of Schedule objects.
    m.schedules = []
    for sch in yaml_obj['schedule']:
        s = schedule.Schedule(sch)
        m.schedules.append(s)

    return m
