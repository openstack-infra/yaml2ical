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
from io import StringIO
import os
import os.path
import pytz
import yaml


from yaml2ical.recurrence import supported_recurrences

DATES = {
    'Monday': datetime.date(1900, 1, 1),
    'Tuesday': datetime.date(1900, 1, 2),
    'Wednesday': datetime.date(1900, 1, 3),
    'Thursday': datetime.date(1900, 1, 4),
    'Friday': datetime.date(1900, 1, 5),
    'Saturday': datetime.date(1900, 1, 6),
    'Sunday': datetime.date(1900, 1, 7),
}
ONE_WEEK = datetime.timedelta(weeks=1)


class SkipDate(object):
    """A date, time and reason to skip a meeting."""

    def __init__(self, date, time, reason):
        date = datetime.datetime.combine(date, time).replace(tzinfo=pytz.utc)
        self.date = date
        self.reason = reason

    @property
    def date_str(self):
        return self.date.strftime("%Y%m%dT%H%M%SZ")


class Schedule(object):
    """A meeting schedule."""

    def __init__(self, meeting, sched_yaml):
        """Initialize schedule from yaml."""

        self.project = meeting.project
        self.filefrom = meeting.filefrom
        # mandatory: time, day, irc, freq, recurrence
        try:
            self.utc = sched_yaml['time']
            self.time = datetime.datetime.strptime(sched_yaml['time'], '%H%M')
            # Sanitize the Day
            self.day = sched_yaml['day'].lower().capitalize()
            self.irc = sched_yaml['irc']
            self.freq = sched_yaml['frequency']
            self.recurrence = supported_recurrences[sched_yaml['frequency']]
        except KeyError as e:
            print("Invalid YAML meeting schedule definition - missing "
                  "attribute '{0}'".format(e.args[0]))
            raise

        # optional: start_date defaults to the current date if not present
        if 'start_date' in sched_yaml:
            try:
                self.start_date = datetime.datetime.strptime(
                    str(sched_yaml['start_date']), '%Y%m%d')
            except ValueError:
                raise ValueError("Could not parse 'start_date' (%s) in %s" %
                                (sched_yaml['start_date'], self.filefrom))
        else:
            self.start_date = datetime.datetime.utcnow()

        # optional: duration
        if 'duration' in sched_yaml:
            try:
                self.duration = int(sched_yaml['duration'])
            except ValueError:
                raise ValueError("Could not parse 'duration' (%s) in %s" %
                                (sched_yaml['duration'], self.filefrom))
        else:
            self.duration = 60

        if self.day not in DATES.keys():
            raise ValueError("'%s' is not a valid day of the week")

        # optional: skip_dates
        # This is a sequence of mappings (YAML)
        # This is a list of dicts (python)
        if 'skip_dates' in sched_yaml:
            self.skip_dates = []
            for skip_date in sched_yaml['skip_dates']:
                missing_keys = set(['skip_date', 'reason']) - set(skip_date)
                if missing_keys:
                    raise KeyError(("Processing: %s Missing keys - %s" %
                                    (self.filefrom, ','.join(missing_keys))))

                # NOTE(tonyb) We need to include the time in an exdate
                # without it the excluded occurrence never matches a
                # scheduled occurrence.
                try:
                    date_str = str(skip_date['skip_date'])
                    date = datetime.datetime.strptime(date_str, '%Y%m%d')
                    self.skip_dates.append(SkipDate(date, self.time.time(),
                                                    skip_date['reason']))
                except ValueError:
                    raise ValueError(("Processing: %s Could not parse "
                                      "skip_date - %s" %
                                      (self.filefrom, skip_date['skip_date'])))

        # NOTE(tonyb): We need to do this datetime shenanigans is so we can
        #              deal with meetings that start on day1 and end on day2.
        self.meeting_start = datetime.datetime.combine(DATES[self.day],
                                                       self.time.time())
        self.meeting_end = (self.meeting_start +
                            datetime.timedelta(minutes=self.duration))
        if self.day == 'Sunday' and self.meeting_end.strftime("%a") == 'Mon':
            self.meeting_start = self.meeting_start - ONE_WEEK
            self.meeting_end = self.meeting_end - ONE_WEEK

    def conflicts(self, other):
        """Checks for conflicting schedules."""
        alternating = set(['biweekly-odd', 'biweekly-even'])
        # NOTE(tonyb): .meeting_start also includes the day of the week. So no
        #              need to check .day explictly
        return ((self.irc == other.irc) and
                ((self.meeting_start < other.meeting_end) and
                 (other.meeting_start < self.meeting_end)) and
                (set([self.freq, other.freq]) != alternating))


class Meeting(object):
    """An online meeting."""

    def __init__(self, data):
        """Initialize meeting from meeting yaml description."""

        yaml_obj = yaml.safe_load(data)

        try:
            self.chair = yaml_obj['chair']
            self.description = yaml_obj['description']
            self.project = yaml_obj['project']
        except KeyError as e:
            print("Invalid YAML meeting definition - missing "
                  "attribute '{0}'".format(e.args[0]))
            raise

        # Find any extra values the user has provided that they might
        # want to have access to in their templates.
        self.extras = {}
        self.extras.update(yaml_obj)
        for k in ['chair', 'description', 'project', 'schedule']:
            if k in self.extras:
                del self.extras[k]

        try:
            self.filefrom = os.path.basename(data.name)
            self.outfile = os.path.splitext(self.filefrom)[0] + '.ics'
        except AttributeError:
            self.filefrom = "stdin"
            self.outfile = "stdin.ics"

        self.schedules = []
        for sch in yaml_obj['schedule']:
            s = Schedule(self, sch)
            self.schedules.append(s)

    @classmethod
    def fromfile(cls, yaml_file):
        f = open(yaml_file, 'r')
        return cls(f)

    @classmethod
    def fromstring(cls, yaml_string):
        s = StringIO(yaml_string)
        return cls(s)


def load_meetings(yaml_source):
    """Build YAML object and load meeting data

    :param yaml_source: source data to load, which can be a directory or
                        stream.
    :returns: list of meeting objects
    """
    meetings = []
    # Determine what the yaml_source is. Files must have .yaml extension
    # to be considered valid.
    if os.path.isdir(yaml_source):
        for root, dirs, files in os.walk(yaml_source):
            for f in files:
                # Build the entire file path and append to the list of yaml
                # meetings
                if os.path.splitext(f)[1] == '.yaml':
                    yaml_file = os.path.join(root, f)
                    meetings.append(Meeting.fromfile(yaml_file))
    elif (os.path.isfile(yaml_source) and
          os.path.splitext(yaml_source)[1] == '.yaml'):
        meetings.append(Meeting.fromfile(yaml_source))
    elif isinstance(yaml_source, str):
        return [Meeting.fromstring(yaml_source)]

    if not meetings:
        # If we don't have a .yaml file, a directory of .yaml files, or any
        # YAML data fail out here.
        raise ValueError("No .yaml file, directory containing .yaml files, "
                         "or YAML data found.")
    else:
        meetings.sort(key=lambda x: x.project)
        return meetings


class MeetingConflictError(Exception):
    pass


def check_for_meeting_conflicts(meetings):
    """Check if a list of meetings have conflicts.

    :param meetings: list of Meeting objects

    """

    for i in range(len(meetings)):
        schedules = meetings[i].schedules
        for j in range(i + 1, len(meetings)):
            other_schedules = meetings[j].schedules
            for schedule in schedules:
                for other_schedule in other_schedules:
                    if schedule.conflicts(other_schedule):
                        msg_dict = {'one': schedule.filefrom,
                                    'two': other_schedule.filefrom}
                        raise MeetingConflictError(
                            "Conflict between %(one)s and %(two)s" % msg_dict)
