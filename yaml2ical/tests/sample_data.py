#! /usr/bin/env python
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

"""Sample meeting data to use for testing."""

WEEKLY_MEETING = """
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

CONFLICTING_WEEKLY_MEETING = """
project: OpenStack Subteam Meeting 2
schedule:
  - time: '1230'
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam 2 project.
agenda: |
  * New features
"""

WEEKLY_OTHER_CHANNEL_MEETING = """
project: OpenStack Subteam Meeting 3
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting-alt
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam 3 project.
agenda: |
  * New features
"""

ALTERNATING_MEETING = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-even
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

BIWEEKLY_EVEN_MEETING = """
project: OpenStack Subteam 12 Meeting
schedule:
  - time: '2200'
    day: Wednesday
    irc: openstack-meeting
    frequency: biweekly-even
chair: Jane Developer
description: >
    Weekly meeting for Subteam project.
agenda: |
  * Top bugs this week
"""

BIWEEKLY_ODD_MEETING = """
project: OpenStack Subteam 12 Meeting
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
