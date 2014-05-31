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
import logging
import os

import icalendar
import pytz
import yaml

from arbiter import const
from arbiter import schedule


class Meeting:
    """An OpenStack meeting."""

    def __init__(self, yaml, filename):
        """Initialize meeting from yaml file name 'filename'."""

        self.filename = filename

        # initialize using yaml
        self.project = yaml['project']
        self.chair = yaml['chair']
        self.description = yaml['description']
        self.agenda = yaml['agenda']  # this is a list of list of topics

        # create schedule objects
        self.schedules = []
        for sch in yaml['schedule']:
            s = schedule.Schedule(sch)
            self.schedules.append(s)

    def write_ical(self, ical_dir):
        """Write this meeting to disk using the iCal format."""

        cal = icalendar.Calendar()

        # add properties to ensure compliance
        cal.add('prodid', '-//OpenStack//Gerrit-Powered Meeting Agendas//EN')
        cal.add('version', '2.0')

        for schedule in self.schedules:
            # one Event per iCal file
            event = icalendar.Event()

            # NOTE(jotan): I think the summary field needs to be unique per
            # event in an ical file (at least, for it to work with
            # Google Calendar)

            event.add('summary', self.project + ' (' + schedule.irc + ')')

            # add ical description
            project_descript = "Project:  %s" % (self.project)
            chair_descript = "Chair:  %s" % (self.chair)
            irc_descript = "IRC:  %s" % (schedule.irc)
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
            next_meeting = self._next_weekday(d, const.WEEKDAYS[schedule.day])

            next_meeting_dt = datetime.datetime(next_meeting.year,
                                                next_meeting.month,
                                                next_meeting.day,
                                                schedule.time.hour,
                                                schedule.time.minute,
                                                tzinfo=pytz.utc)
            event.add('dtstart', next_meeting_dt)

            # add recurrence rule
            event.add('rrule', {'freq': schedule.freq})

            # add meeting length
            # TODO(jotan): determine duration to use for OpenStack meetings
            event.add('duration', datetime.timedelta(hours=1))

            # add event to calendar
            cal.add_component(event)

        # determine file name from source file
        ical_filename = os.path.basename(self.filename).split('.')[0] + '.ics'
        ical_filename = os.path.join(ical_dir, ical_filename)

        if not os.path.exists(ical_dir):
            os.makedirs(ical_dir)

        # write ical files to disk
        with open(ical_filename, 'wb') as ics:
            ics.write(cal.to_ical())

        num_events = len(cal.subcomponents)
        logging.info("Wrote %(num_events)d event(s) to file '%(ical_file)s'" %
                     {'ical_file': ical_filename,
                      'num_events': num_events})

    def get_schedule_tuple(self):
        """returns a list of meeting tuples consisting meeting name, meeting
        time, day, and irc room.

        :returns: list of meeting tuples

        """

        meetings = []
        for schedule in self.schedules:
            schedule_time = schedule.time.hour * 100 + schedule.time.minute
            meetings.append((self.filename,
                             (schedule_time,
                              schedule.day,
                              schedule.irc)))
        return meetings

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
