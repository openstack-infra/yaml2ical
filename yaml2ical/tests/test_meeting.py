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

import re
import unittest

from yaml2ical import ical
from yaml2ical import meeting
from yaml2ical.tests import sample_data


class MeetingTestCase(unittest.TestCase):

    def test_bad_meeting_day(self):
        self.assertRaises(ValueError,
                          meeting.load_meetings,
                          sample_data.BAD_MEETING_DAY)

    def test_load_yaml_file(self):
        m = meeting.load_meetings(sample_data.WEEKLY_MEETING)[0]
        self.assertEqual('OpenStack Subteam Meeting', m.project)
        self.assertEqual('Joe Developer', m.chair)
        self.assertEqual('Weekly meeting for Subteam project.\n',
                         m.description)

    def should_be_conflicting(self, yaml1, yaml2):
        """Exception is raised when meetings should conflict."""
        meeting_one = meeting.load_meetings(yaml1)
        meeting_two = meeting.load_meetings(yaml2)
        meeting_list = [meeting_one.pop(), meeting_two.pop()]
        self.assertRaises(meeting.MeetingConflictError,
                          meeting.check_for_meeting_conflicts,
                          meeting_list)

    def should_not_conflict(self, yaml1, yaml2):
        """No exception raised when meetings shouldn't conflict."""
        meeting_one = meeting.load_meetings(yaml1)
        meeting_two = meeting.load_meetings(yaml2)
        meeting_list = [meeting_one.pop(), meeting_two.pop()]
        meeting.check_for_meeting_conflicts(meeting_list)

    def test_weekly_conflict(self):
        self.should_be_conflicting(
            sample_data.WEEKLY_MEETING,
            sample_data.CONFLICTING_WEEKLY_MEETING)
        self.should_not_conflict(
            sample_data.WEEKLY_MEETING,
            sample_data.WEEKLY_OTHER_CHANNEL_MEETING)

    def test_biweekly_conflict(self):
        self.should_be_conflicting(
            sample_data.WEEKLY_MEETING,
            sample_data.ALTERNATING_MEETING)
        self.should_not_conflict(
            sample_data.ALTERNATING_MEETING,
            sample_data.BIWEEKLY_EVEN_MEETING)
        self.should_be_conflicting(
            sample_data.ALTERNATING_MEETING,
            sample_data.BIWEEKLY_ODD_MEETING)
        self.should_not_conflict(
            sample_data.BIWEEKLY_ODD_MEETING,
            sample_data.BIWEEKLY_EVEN_MEETING)

    def test_late_early_conflicts(self):
        self.should_be_conflicting(
            sample_data.MEETING_SUNDAY_LATE,
            sample_data.MEETING_MONDAY_EARLY)
        self.should_be_conflicting(
            sample_data.MEETING_MONDAY_LATE,
            sample_data.MEETING_TUESDAY_EARLY)

    def test_meeting_duration(self):
        m = meeting.load_meetings(sample_data.MEETING_WITH_DURATION)[0]
        self.assertEqual(30, m.schedules[0].duration)
        m = meeting.load_meetings(sample_data.WEEKLY_MEETING)[0]
        self.assertEqual(60, m.schedules[0].duration)

    def test_short_meeting_conflicts(self):
        self.should_be_conflicting(
            sample_data.WEEKLY_MEETING,
            sample_data.MEETING_WITH_DURATION)
        self.should_not_conflict(
            sample_data.CONFLICTING_WEEKLY_MEETING,
            sample_data.MEETING_WITH_DURATION)

    def test_skip_meeting(self):
        meeting_yaml = sample_data.MEETING_WITH_SKIP_DATES
        # Copied from sample_data.MEETING_WITH_SKIP_DATES
        summary = 'OpenStack Subteam 8 Meeting'
        patterns = []
        # The "main" meeting should have an exdate
        patterns.append(re.compile('.*exdate:\s*20150810T120000', re.I))
        # The "main" meeting should start on 2015-08-13
        patterns.append(re.compile('.*dtstart;.*:20150803T120000Z', re.I))
        # The "main" meeting should have a simple summary
        patterns.append(re.compile('.*summary:\s*%s' % summary, re.I))
        # The "skipped" meeting should start on 20150806
        patterns.append(re.compile('.*dtstart;.*:20150810T120000Z', re.I))
        # The "skipped" meeting should say include 'CANCELLED' and the datetime
        patterns.append(re.compile('.*summary:\s*CANCELLED.*20150810T120000Z',
                                   re.I))
        m = meeting.load_meetings(meeting_yaml)[0]
        cal = ical.Yaml2IcalCalendar()
        cal.add_meeting(m)
        cal_str = str(cal.to_ical())
        self.assertTrue(hasattr(m.schedules[0], 'skip_dates'))
        for p in patterns:
            self.assertNotEqual(None, p.match(cal_str))

    def test_skip_meeting_missing_skip_date(self):
        self.assertRaises(KeyError,
                          meeting.load_meetings,
                          sample_data.MEETING_WITH_MISSING_SKIP_DATE)

    def test_skip_meeting_missing_reason(self):
        self.assertRaises(KeyError,
                          meeting.load_meetings,
                          sample_data.MEETING_WITH_MISSING_REASON)

    def test_skip_meeting_bad_skip_date(self):
        self.assertRaises(ValueError,
                          meeting.load_meetings,
                          sample_data.MEETING_WITH_SKIP_DATES_BAD_DATE)
