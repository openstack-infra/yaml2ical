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

    def next_meeting(self, to_test):
        test_time = datetime.datetime(2014, 10, 5, 2, 47, 28, 832666)
        test_weekday = 'Wednesday'
        return to_test.next_occurence(test_time, test_weekday)

    def test_next_weekly(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 8, 2, 47, 28, 832666),
            self.next_meeting(recurrence.WeeklyRecurrence()))

    def test_next_biweekly_odd(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 8, 2, 47, 28, 832666),
            self.next_meeting(recurrence.BiWeeklyRecurrence(style='odd')))

    def test_next_biweekly_even(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 15, 2, 47, 28, 832666),
            self.next_meeting(recurrence.BiWeeklyRecurrence(style='even')))

    def test_next_quadweekly_week_0(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 29, 2, 47, 28, 832666),
            self.next_meeting(recurrence.QuadWeeklyRecurrence(week=0)))

    def test_next_quadweekly_week_1(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 8, 2, 47, 28, 832666),
            self.next_meeting(recurrence.QuadWeeklyRecurrence(week=1)))

    def test_next_quadweekly_week_2(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 15, 2, 47, 28, 832666),
            self.next_meeting(recurrence.QuadWeeklyRecurrence(week=2)))

    def test_next_quadweekly_week_3(self):
        self.assertEqual(
            datetime.datetime(2014, 10, 22, 2, 47, 28, 832666),
            self.next_meeting(recurrence.QuadWeeklyRecurrence(week=3)))

    def test_next_adhoc(self):
        self.assertEqual(
            None,
            self.next_meeting(recurrence.AdhocRecurrence()))

    def test_weekly_str(self):
        self.assertEqual(
            'Weekly',
            str(recurrence.WeeklyRecurrence()))

    def test_biweekly_odd_str(self):
        self.assertEqual(
            'Every two weeks (on odd weeks)',
            str(recurrence.BiWeeklyRecurrence(style='odd')))

    def test_biweekly_even_str(self):
        self.assertEqual(
            'Every two weeks (on even weeks)',
            str(recurrence.BiWeeklyRecurrence(style='even')))

    def test_quadweekly_str(self):
        for i in range(4):
            self.assertEqual(
                'Every four weeks on week %d of the four week rotation' % i,
                str(recurrence.QuadWeeklyRecurrence(week=i)))
