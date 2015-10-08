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

BAD_MEETING_DAY = """
project: OpenStack Subteam Meeting
schedule:
  - time: '1200'
    day: go_bang
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly meeting for Subteam project.
"""

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

MEETING_SUNDAY_LATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '2330'
    day: Sunday
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly late meeting for Subteam 8 project.
"""

MEETING_MONDAY_EARLY = """
project: OpenStack Subteam Meeting
schedule:
  - time: '0000'
    day: Monday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly long meeting for Subteam project.
"""

MEETING_MONDAY_LATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '2330'
    day: Monday
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly late meeting for Subteam 8 project.
"""

MEETING_TUESDAY_EARLY = """
project: OpenStack Subteam Meeting
schedule:
  - time: '0000'
    day: Tuesday
    irc: openstack-meeting
    frequency: weekly
chair: Joe Developer
description: >
    Weekly long meeting for Subteam project.
"""

MEETING_WITH_DURATION = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    duration: 30
    day: Wednesday
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
agenda: |
  * Debate whether this should be a longer meeting
"""

MEETING_WITH_START_DATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    duration: 30
    day: Thursday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
agenda: |
  * Debate whether this should be a longer meeting
"""

MEETING_WITH_SKIP_DATES = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skip_date: 20150810
          reason: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

MEETING_WITH_SKIP_DATES_BAD_DATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skip_date: 2015080
          reason: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

# typo in skip_date
MEETING_WITH_MISSING_SKIP_DATE = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skiip_date: 20150806
          reason: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""

# typo in reason
MEETING_WITH_MISSING_REASON = """
project: OpenStack Subteam 8 Meeting
schedule:
  - time: '1200'
    day: Monday
    start_date: 20150801
    irc: openstack-meeting
    frequency: weekly
    skip_dates:
        - skip_date: 20150806
          reaso: Chair on vacation
chair: Shannon Stacker
description: >
    Weekly short meeting for Subteam project.
"""
