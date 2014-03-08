import pprint
import pytz
import icalendar
import datetime
import time
import os
import yaml
import logging

weekdays = {  
           'Monday'    : 0
         , 'Tuesday'   : 1
         , 'Wednesday' : 2
         , 'Thursday'  : 3
         , 'Friday'    : 4
         , 'Saturday'  : 5
         , 'Sunday'    : 6
         }

class Meeting:
    """An OpenStack meeting."""

    def __init__(self, yaml, filename):

        self.filename = filename

        # create yaml object from yaml file. use it initialize following fields.
        self.project = yaml['project']
        self.chair = yaml['chair']
        self.description = yaml['description']
        self.agenda = yaml['agenda'] # this is a list of list of topics

        # create schedule objects
        self.schedules = [Schedule(s) for s in yaml['schedule']]

    def write_ical(self):
        cal = icalendar.Calendar()

        # add properties to ensure compliance
        cal.add('prodid', '-//OpenStack//Gerrit-Powered Meeting Agendas//EN')
        cal.add('version', '2.0')

        i = 1
        for s in self.schedules:
            # one Event per iCal file
            event = icalendar.Event()
            # I think the summary field needs to be unique per event in an ical file (at least, for it to work with Google Calendar)
            event.add('summary', self.project + ' ' + str(i))

            # add ical description (meeting description, irc, agenda, chair, etc.)
            ical_descript = "Project:  %s\nChair:  %s\nIRC:  %s\nAgenda:\n%s\n\nDescription:  %s" % (self.project, self.chair, s.irc, yaml.dump(self.agenda, default_flow_style=False), self.description)
            event.add('description', ical_descript)

            # get starting date
            d = datetime.datetime.utcnow()
            next_meeting = next_weekday(d, weekdays[s.day]) # 0 = Monday, 1=Tuesday, 2=Wednesday...

            next_meeting_dt = datetime.datetime(next_meeting.year, next_meeting.month, next_meeting.day, s.time.hour, s.time.minute, tzinfo=pytz.utc)
            event.add('dtstart', next_meeting_dt)

            # add recurrence rule
            event.add('rrule', {'freq': s.freq})

            # add meeting length
            # TODO: figure out what to do for meeting length. doesn't seem to be specified for any of the openstack meetings
            event.add('duration', datetime.timedelta(hours=1))

            # add event to calendar
            cal.add_component(event)
            i += 1
        
        # write ical files to disk
        ical_dir = '../icals'
        ical_filename = self.filename[:-4] + 'ics'

        if not os.path.exists(ical_dir):
            os.makedirs(ical_dir)
        os.chdir(ical_dir)

        with open(ical_filename, 'wb') as ics:
            ics.write(cal.to_ical())

        logging.info('\'%s\' processed. Contains %d events.' % (ical_filename, len(cal.subcomponents)))

class Schedule:
    """A meeting schedule."""

    def __init__(self, sched_yaml):
        self.time = datetime.datetime.strptime(sched_yaml['time'], '%H%M')
        self.day = sched_yaml['day']
        self.irc = sched_yaml['irc']
        self.freq = sched_yaml['frequency']

# https://stackoverflow.com/questions/6558535/python-find-the-date-for-the-first-monday-after-a-given-a-date
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
