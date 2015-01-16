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

import unittest

from yaml2ical import meeting
from yaml2ical.tests import sample_data


class MeetingTestCase(unittest.TestCase):

    def test_load_yaml_file(self):
        m = meeting.load_meetings(sample_data.FIRST_MEETING_YAML)[0]
        self.assertEqual('OpenStack Subteam Meeting', m.project)
        self.assertEqual('Joe Developer', m.chair)
        self.assertEqual('Weekly meeting for Subteam project.\n',
                         m.description)

    def test_exception_raised_when_conflict_detected(self):
        """Exception is raised when a meeting conflict is detected."""
        meeting_one = meeting.load_meetings(sample_data.FIRST_MEETING_YAML)
        meeting_two = meeting.load_meetings(sample_data.SECOND_MEETING_YAML)
        meeting_list = [meeting_one.pop(), meeting_two.pop()]
        self.assertRaises(meeting.MeetingConflictError,
                          meeting.check_for_meeting_conflicts,
                          meeting_list)

    def test_no_exception_raised_with_diff_irc_rooms(self):
        """No exception raised when using different IRC rooms."""
        meeting_one = meeting.load_meetings(sample_data.FIRST_MEETING_YAML)
        meeting_two = meeting.load_meetings(sample_data.THIRD_MEETING_YAML)
        meeting_list = [meeting_one.pop(), meeting_two.pop()]
        meeting.check_for_meeting_conflicts(meeting_list)
