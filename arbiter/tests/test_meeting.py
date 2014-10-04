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
import unittest

from arbiter import meeting

_MEETING_YAML = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

_BIWEEKLY_MEETING_YAML = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-even
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-odd
chair: Jane Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""


class MeetingTestCase(unittest.TestCase):

    def test_load_yaml_file(self):
        m = meeting.load_meetings(_MEETING_YAML)[0]
        self.assertEqual('OpenStack Subteam Meeting', m.project)
        self.assertEqual('Joe Developer', m.chair)
        self.assertEqual('Weekly meeting for Subteam project.\n',
                         m.description)
        self.assertEqual('* Top bugs this week\n', m.agenda)

    def test_calculate_next_biweekly_meeting_meet_on_even(self):
        test_time = datetime.datetime(2014, 10, 5, 2, 47, 28, 832666)
        test_weekday = 2
        meet_on_even = True
        next_meeting = meeting.next_biweekly_meeting(test_time,
                                                     test_weekday,
                                                     meet_on_even=meet_on_even)
        expected_meeting = datetime.datetime(2014, 10, 8, 2, 47, 28, 832666)
        self.assertEqual(expected_meeting, next_meeting)
