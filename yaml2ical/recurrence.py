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


WEEKDAYS = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6}


def next_weekday(ref_date, day):
    """Return the date of the next meeting.

    :param ref_date: datetime object of meeting
    :param day: weekday the meeting is held on

    :returns: datetime object of the next meeting time
    """

    weekday = WEEKDAYS[day]
    days_ahead = weekday - ref_date.weekday()
    if days_ahead <= 0:  # target day already happened this week
        days_ahead += 7
    return ref_date + datetime.timedelta(days_ahead)


def next_biweekly_meeting(current_date_time, day, meet_on_even=False):
    """Calculate the next biweekly meeting.

    :param current_date_time: the current datetime object
    :param day: scheduled day of the meeting
    :param meet_on_even: True if meeting on even weeks and False if meeting
    on odd weeks
    :returns: datetime object of next meeting

    """
    weekday = WEEKDAYS[day]
    first_day_of_mo = current_date_time.replace(day=1)
    day_of_week = first_day_of_mo.strftime("%w")
    adjustment = (8 - int(day_of_week)) % (7 - weekday)
    if meet_on_even:
        adjustment += 7
    next_meeting = first_day_of_mo + datetime.timedelta(adjustment)

    if current_date_time > next_meeting:
        next_meeting = next_meeting + datetime.timedelta(14)
        if current_date_time > next_meeting:
            current_date_time = current_date_time.replace(
                month=current_date_time.month + 1, day=1)
            first_wday_next_mo = next_weekday(current_date_time, weekday)
            if meet_on_even:
                next_meeting = first_wday_next_mo + datetime.timedelta(7)
            else:
                next_meeting = first_wday_next_mo
    return next_meeting
