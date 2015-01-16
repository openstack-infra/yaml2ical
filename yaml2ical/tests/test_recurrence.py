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

from yaml2ical import recurrence


class RecurrenceTestCase(unittest.TestCase):

    def test_calculate_next_biweekly_meeting_meet_on_even(self):
        test_time = datetime.datetime(2014, 10, 5, 2, 47, 28, 832666)
        test_weekday = 'Wednesday'
        meet_on_even = True
        next_meeting = recurrence.next_biweekly_meeting(
            test_time,
            test_weekday,
            meet_on_even=meet_on_even)
        expected_meeting = datetime.datetime(2014, 10, 8, 2, 47, 28, 832666)
        self.assertEqual(expected_meeting, next_meeting)
