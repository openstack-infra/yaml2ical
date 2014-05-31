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

import unittest

from arbiter import meeting

_YAML = """
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


class MeetingTestCase(unittest.TestCase):

    def test_load_yaml_file(self):
        m = meeting.load_meetings(_YAML)[0]
        self.assertEqual('OpenStack Subteam Meeting', m.project)
        self.assertEqual('Joe Developer', m.chair)
        self.assertEqual('Weekly meeting for Subteam project.\n',
                         m.description)
        self.assertEqual('* Top bugs this week\n', m.agenda)
