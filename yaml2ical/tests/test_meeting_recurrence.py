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
import unittest

from yaml2ical import meeting
from yaml2ical import recurrence
from yaml2ical.tests import sample_data


class Meeting_RecurrenceTestCase(unittest.TestCase):

    def test_next_meeting_start_date(self):
        m = meeting.load_meetings(sample_data.MEETING_WITH_START_DATE)[0]
        self.assertEqual(
            datetime.datetime(2015, 8, 6, 0, 0),
            recurrence.WeeklyRecurrence().next_occurence(
                m.schedules[0].start_date, m.schedules[0].day))
