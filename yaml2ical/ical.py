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
import icalendar
import logging
import os
import pytz

from yaml2ical import meeting
from yaml2ical import recurrence


class Yaml2IcalCalendar(icalendar.Calendar):
    """A calendar in ics format."""

    def __init__(self):
        super(Yaml2IcalCalendar, self).__init__()
        self.add('prodid', '-//yaml2ical agendas//EN')
        self.add('version', '2.0')

    def add_meeting(self, meeting):
        """Add this meeting to the calendar."""

        for sch in meeting.schedules:
            # one Event per iCal file
            event = icalendar.Event()

            # NOTE(jotan): I think the summary field needs to be unique per
            # event in an ical file (at least, for it to work with
            # Google Calendar)

            event.add('summary', meeting.project)
            event.add('location', '#' + sch.irc)

            # add ical description
            project_descript = "Project:  %s" % (meeting.project)
            chair_descript = "Chair:  %s" % (meeting.chair)
            descript_descript = "Description:  %s" % (meeting.description)
            ical_descript = "\n".join((project_descript,
                                       chair_descript,
                                       descript_descript))
            event.add('description', ical_descript)

            # get starting date
            start_date = datetime.datetime.utcnow()
            if sch.freq.startswith('biweekly'):
                meet_on_even = sch.freq.endswith('even')
                next_meeting = recurrence.next_biweekly_meeting(
                    start_date,
                    sch.day,
                    meet_on_even=meet_on_even)
            else:
                next_meeting = recurrence.next_weekday(start_date, sch.day)

            next_meeting_date = datetime.datetime(next_meeting.year,
                                                  next_meeting.month,
                                                  next_meeting.day,
                                                  sch.time.hour,
                                                  sch.time.minute,
                                                  tzinfo=pytz.utc)
            event.add('dtstart', next_meeting_date)

            # add recurrence rule
            if sch.freq.startswith('biweekly'):
                cadence = ()
                # NOTE(lbragstad): Setting the `cadence` for the schedule
                # will allow for alternating meetings. Typically there are
                # only 4 weeks in a month but adding `5` and `6` allow for
                # cases where there are 5 meetings in a month, which would
                # otherwise be unsupported if only setting `cadence` to
                # either (1, 3) or (2, 4).
                if sch.freq == 'biweekly-odd':
                    cadence = (1, 3, 5)
                elif sch.freq == 'biweekly-even':
                    cadence = (2, 4, 6)
                rule_dict = {'freq': 'monthly',
                             'byday': sch.day[0:2],
                             'bysetpos': cadence}
                event.add('rrule', rule_dict)
            else:
                event.add('rrule', {'freq': sch.freq})

            # add meeting length
            # TODO(jotan): determine duration to use for OpenStack meetings
            event.add('duration', datetime.timedelta(hours=1))

            # add event to calendar
            self.add_component(event)

    def write_to_disk(self, filename):
        # write ical files to disk
        with open(filename, 'wb') as ics:
            ics.write(self.to_ical())


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
    meeting.check_for_meeting_conflicts(meetings)

    # convert meetings to a list of ical
    if outputdir:
        for m in meetings:
            cal = Yaml2IcalCalendar()
            cal.add_meeting(m)
            filename = m.filefrom.split('.')[0] + '.ics'
            cal.write_to_disk(os.path.join(outputdir, filename))

    # convert meetings into a single ical
    if outputfile:
        cal = Yaml2IcalCalendar()
        for m in meetings:
            cal.add_meeting(m)
        cal.write_to_disk(outputfile)

    # TODO(jotan): verify converted ical is valid
    logging.info('Wrote %d meetings to iCal' % (len(meetings)))
