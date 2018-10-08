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

import calendar
import datetime


WEEKDAYS = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6}


class WeeklyRecurrence(object):
    """Meetings occuring every week."""
    def __init__(self):
        pass

    def next_occurence(self, current_date_time, day):
        """Return the date of the next meeting.

        :param ref_date: datetime object of meeting
        :param day: weekday the meeting is held on

        :returns: datetime object of the next meeting time
        """

        weekday = WEEKDAYS[day]
        days_ahead = weekday - current_date_time.weekday()
        if days_ahead < 0:  # target day already happened this week
            days_ahead += 7
        return current_date_time + datetime.timedelta(days_ahead)

    def rrule(self):
        return {'freq': 'weekly'}

    def __str__(self):
        return "Weekly"


class BiWeeklyRecurrence(object):
    """Meetings occuring on alternate weeks.

    Can be either on odd weeks or on even weeks
    """
    def __init__(self, style='even'):
        self.style = style

    def next_occurence(self, current_date, day):
        """Calculate the next biweekly meeting.

        :param current_date: the current date
        :param day: scheduled day of the meeting
        :returns: datetime object of next meeting
        """
        nextweek_day = WeeklyRecurrence().next_occurence(current_date, day)
        if nextweek_day.isocalendar()[1] % 2:
            # ISO week is odd
            if self.style == 'odd':
                return nextweek_day
        else:
            # ISO week is even
            if self.style == 'even':
                return nextweek_day
        # If week doesn't match rule, skip one week
        return nextweek_day + datetime.timedelta(7)

    def rrule(self):
        return {'freq': 'weekly', 'interval': 2}

    def __str__(self):
        return "Every two weeks (on %s weeks)" % self.style


class QuadWeeklyRecurrence(object):
    """Meetings occuring every 4 weeks.

    A week number can be supplied to offset meetings
    """
    def __init__(self, week=0):
        self.week = week

    def next_occurence(self, current_date, day):
        """Calculate the next biweekly meeting.

        :param current_date: the current date
        :param day: scheduled day of the meeting
        :returns: datetime object of next meeting
        """
        nextweek_day = WeeklyRecurrence().next_occurence(current_date, day)
        if nextweek_day.isocalendar()[1] % 4 == self.week:
            return nextweek_day
        # If week doesn't match rule, skip one week
        return self.next_occurence(nextweek_day + datetime.timedelta(7), day)

    def rrule(self):
        return {'freq': 'weekly', 'interval': 4}

    def __str__(self):
        return (
            "Every four weeks on week %d of the four week rotation"
            % self.week)


class AdhocRecurrence(object):
    """Meetings occuring as needed.

    Effectively this is a noop recurrance as next_occurance is always None
    """
    def __init__(self):
        pass

    def next_occurence(self, current_date, day):
        """Calculate the next adhoc meeting.

        :param current_date: the current date
        :param day: scheduled day of the meeting
        :returns: datetime object of next meeting
        """
        return None

    def rrule(self):
        return {'freq': 'adhoc', 'interval': 0}

    def __str__(self):
        return "Occurs as needed, no fixed schedule."


class MonthlyRecurrence(object):
    """Meetings occuring every month."""
    def __init__(self, week, day):
        self._week = week
        self._day = day

    def next_occurence(self, current_date_time, day):
        """Return the date of the next meeting.

        :param current_date_time: datetime object of meeting
        :param day: weekday the meeting is held on

        :returns: datetime object of the next meeting time
        """
        weekday = WEEKDAYS[day]

        month = current_date_time.month + 1
        year = current_date_time.year
        if current_date_time.month == 12:
            month = 1
            year = year + 1
        next_month_dates = calendar.monthcalendar(year, month)

        # We can't simply index into the dates for the next month
        # because we don't know that the first week is full of days
        # that actually appear in that month. Therefore we loop
        # through them counting down until we've skipped enough weeks.
        skip_weeks = self._week - 1
        for week in next_month_dates:
            day = week[weekday]
            # Dates in the week that fall in other months
            # are 0 so we want to skip counting those weeks.
            if not day:
                continue
            # If we have skipped all of the weeks we need to,
            # we have the day.
            if not skip_weeks:
                return datetime.datetime(
                    year, month, day,
                    current_date_time.hour, current_date_time.minute,
                    current_date_time.second, current_date_time.microsecond,
                )
            skip_weeks -= 1

        raise ValueError(
            'Could not compute week {} of next month for {}'.format(
                self._week, current_date_time)
        )

    def rrule(self):
        return {
            'freq': 'monthly',
            'byday': '{}{}'.format(self._week, self._day[:2].upper()),
        }

    def __str__(self):
        return "Monthly"


supported_recurrences = {
    'weekly': WeeklyRecurrence(),
    'biweekly-odd': BiWeeklyRecurrence(style='odd'),
    'biweekly-even': BiWeeklyRecurrence(),
    'quadweekly': QuadWeeklyRecurrence(week=0),
    'quadweekly-week-1': QuadWeeklyRecurrence(week=1),
    'quadweekly-week-2': QuadWeeklyRecurrence(week=2),
    'quadweekly-week-3': QuadWeeklyRecurrence(week=3),
    'quadweekly-alternate': QuadWeeklyRecurrence(week=2),
    'adhoc': AdhocRecurrence(),
    'first-monday': MonthlyRecurrence(week=1, day='Monday'),
    'first-tuesday': MonthlyRecurrence(week=1, day='Tuesday'),
    'first-wednesday': MonthlyRecurrence(week=1, day='Wednesday'),
    'first-thursday': MonthlyRecurrence(week=1, day='Thursday'),
    'first-friday': MonthlyRecurrence(week=1, day='Friday'),
}
